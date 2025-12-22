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

**Decrypt a backup file and display QR codes in terminal:**
```bash
uv run python -m decrypt_otpauth.main --p <YOUR .otpauth LOCATION>
```

The tool will ask for your password and display QR codes for each account.

**Save QR codes as images:**
```bash
uv run python -m decrypt_otpauth.main --p <YOUR .otpauth LOCATION> --images-location <OUTPUT_DIRECTORY>
```

This will save QR codes as PNG images in the specified directory instead of displaying them in the terminal.
Each image is named using the account label with a unique hash (e.g., `Google_Account_a1b2c3.png`).

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
