# Volvo-Dashboard

| DATA           | PRIO | CAN ID | OFFSET |
|----------------|------|--------|--------|
| RPM            | LOW  | 0x520  | 0      |
| TPS            | MID  | 0x520  | 2      |
| MAP            | HI   | 0x520  | 4      |
| Lambda/AFR     | HI   | 0x520  | 6      |
| IA             | MID  | 0x521  | 4      |
| KM/H           | LOW  | NO     | NO     |
| Lambda corr A  | MID  | 0x524  | 2      |
| Voltage        | MID  | 0x530  | 0      |
| IAT            | HI   | 0x530  | 4      |
| CT             | MID  | 0x530  | 6      |
| Ethanol%       | MID  | 0x531  | 2      |
| EGT            | HI   | 0x531  | 6      |
| OP             | HI   | 0x536  | 4      |
| OT             | HI   | 0x536  | 6      |
| Lambda target  | LOW  | 0x527  | 6      |
| Error count    | HI   | 0x534  | 4      |



# Data on Page 1

| DATA |
|------|
| MAP  |
| AFR  |
| IAT  |
| EGT  |
| OP   |
| OT   |