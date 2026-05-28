# Korean Privacy Rule Coverage

This rule set is based on Korean privacy categories that are stable enough to encode as deterministic safety-net patterns.

## Official categories used

- Unique identifiers: resident registration number, passport number, driver license number, foreigner registration number. Source: National Law Information Center, Personal Information Protection Act Enforcement Decree Article 19.
- Personal information examples include name, resident registration number, and images that can identify a living individual. Source: National Law Information Center, Personal Information Protection Act interpretation material.
- Risk classification examples include authentication information such as passwords and biometric information, financial information such as card numbers and account numbers, location information, address, phone number, email address, birth date, IP information, MAC address, and internal identifiers such as employee/member numbers. Source: National Law Information Center privacy-information type table.

## Implemented deterministic coverage

- Unique identifiers: Korean resident/foreigner registration number, passport number, driver license number.
- Organization identifiers often entered with personal records: business registration number and corporate registration number.
- Contact and location: Korean mobile/landline/050 numbers, international `+82` phone forms, road-name and lot-number addresses, postal code in address context, GPS coordinate context.
- Financial/authentication: bank account, card number, card CVC/CVV, OTP/PIN/authentication code, API keys and Slack-style tokens.
- Online/communication identifiers: email, obfuscated email forms, URL/domain in URL context, IP address, MAC address.
- Internal identifiers: login ID, student number, employee number, member/customer/patient/chart/exam/military numbers in explicit context.

## Boundary

The regex safety net intentionally does not claim universal coverage. It is a high-recall deterministic layer that must be paired with context suppression and evaluation. Values that look like PII but are marked as model names, sample data, placeholders, or document versions are suppressed to reduce hard-negative false positives.
