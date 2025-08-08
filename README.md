# Decrypt OTP Auth

Decrypt backup files created by [OTP Auth for iOS](https://apps.apple.com/us/app/otp-auth/id659877384).

This is an updated version of [CooperRS/decrypt-otpauth-files](https://github.com/CooperRS/decrypt-otpauth-files) with modern Python support.

## Installation

```bash
git clone https://github.com/wenceslas-sanchez/decrypt-otpauth.git
cd decrypt-otpauth
uv sync
```

## Usage

**Decrypt a backup file:**
```bash
uv run python decrypt_otpauth.py decrypt_backup --encrypted-otpauth-backup backup.otpauthdb
```

**Decrypt a single account:**
```bash
uv run python decrypt_otpauth.py decrypt_account --encrypted-otpauth-account account.otpauth
```

The tool will ask for your password and display QR codes for each account.

## Requirements

- Python 3.13+
- Your OTP Auth backup files and password

## What's New

- Updated for modern Python versions
- Improved error handling
- Better security practices
- Cleaner code structure
- Reduced dependencies on non-standard packages

## License

GPL-3.0 License
