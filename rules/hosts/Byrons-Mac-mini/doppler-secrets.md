# Secret management: Doppler for admin keys, SSM Parameter Store for projects

Never store secrets in plaintext files, `.env` files, or committed configs.

## Two layers

```
Doppler (admin only, two projects, never more)
├── global / home              Byron's admin keys shared across machines and tools
│                              e.g. OPENAI_API_KEY, CLOUDFLARE_API_TOKEN, GH_TOKEN, AWS_*
└── northwindcapital / admin   North Wind Capital company-level keys and reference IDs

AWS SSM Parameter Store (one path per repo, in the account that owns the repo)
└── /<project>/<env>/<KEY>     SecureString, env is dev or prd, KEY is what the code reads
                               the project's runbook/dependencies.md lists its keys
```

**Doppler is for personal and company infrastructure** - keys a human uses across tools and
machines, and the bootstrap for everything else. Code never reads from Doppler. Do not create
Doppler projects; the two above are the whole list.

**Parameter Store is for repos** - each repo's scoped keys live under its own path, provisioned
from the admin keys, in `ap-southeast-2`. Parameters are created and rotated only with
`aws ssm put-parameter`, never through Terraform: the `aws_ssm_parameter` resource reads the
decrypted value into state on every refresh, whatever `ignore_changes` says. Terraform manages
the IAM that reads a path, nothing else; the project's runbook lists which keys exist.

## Key scoping rules

- **Assume admin scope**: keys in `global/home` and `northwindcapital/admin` are provisioned with
  broad permissions. Never use them directly in project code, containers or CI.
- **Create scoped keys for projects**: use the admin key once to provision a narrowly-scoped key,
  then store that under the project's SSM path.
- **Principle of least privilege**: the project key has exactly the access the project needs.
  Workloads read their own path with an IAM identity limited to `ssm:GetParametersByPath` and
  `kms:Decrypt` on that path; GitHub Actions assumes a role through OIDC.
- **Why**: if a scoped key leaks, the blast radius is one path. An admin key leak is the account.

## On-demand access

Secrets are not auto-loaded into the shell. Fetch them explicitly when needed.

**Run a command with admin keys injected:**
```sh
doppler run --project global --config home -- <command>
```

**Run a command with a project's secrets injected:**
```sh
doppler run --project global --config home -- chamber exec <project>/<env> -- <command>
```

**Write or rotate a project secret** (the value goes through a 0600 file, never argv):
```sh
doppler run --project global --config home -- \
  aws ssm put-parameter --region ap-southeast-2 --cli-input-json file://<tmp>.json
```

**List what a project has, names only:**
```sh
doppler run --project global --config home -- \
  aws ssm describe-parameters --region ap-southeast-2 \
  --parameter-filters "Key=Path,Option=Recursive,Values=/<project>" --query 'Parameters[].Name'
```

Never print a secret value into a terminal, a log, a commit or chat; compare hashes when a copy
has to be verified.

## Setup

**New machine**: install Doppler (`brew install dopplerhq/cli/doppler`) and run `doppler login`;
install chamber (`brew install chamber`). Handled by `setup_macos.sh`.

**Headless machines**: set `DOPPLER_TOKEN` to a Doppler service token for `global/home`, or give
the machine an IAM identity for its paths. The Doppler CLI checks that variable automatically.

## Never revoke, delete, or rotate credentials without explicit instruction

Revoking a credential is irreversible. Do not revoke, delete, or rotate any key - even one that
appears superseded or unused - unless explicitly asked. The key may be in use by other tools,
sessions, or people outside your visibility.
