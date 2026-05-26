| type                     | id           | input                                                 | masked                                             | explanation                                 |
|:-------------------------|:-------------|:------------------------------------------------------|:---------------------------------------------------|:--------------------------------------------|
| success                  | chat_0001    | 주민번호는 900101-1234567이고 절대 공유하지 마.       | 주민번호는 <ACCOUNT_NUMBER>이고 절대 공유하지 마.  | 정형 개인정보를 올바르게 마스킹             |
| success                  | chat_0002    | 사업자번호 123-45-67890 이거 세금계산서용이야.        | 사업자번호 <ACCOUNT_NUMBER> 이거 세금계산서용이야. | 정형 개인정보를 올바르게 마스킹             |
| success                  | chat_0012    | 우리 집 전화번호 010-4444-5555도 등록해줘.            | 우리 집 전화번호 <PRIVATE_PHONE>도 등록해줘.       | 정형 개인정보를 올바르게 마스킹             |
| success                  | chat_0019    | 비밀번호는 xoxb-1234567890-abcdefg으로 임시 설정했어. | 비밀번호는 <SECRET>으로 임시 설정했어.             | 정형 개인정보를 올바르게 마스킹             |
| limitation_hard_negative | hardneg_0001 | 모델명은 900101-1234567-A입니다.                      | 모델명은 <ACCOUNT_NUMBER>입니다.                   | 실제 개인정보가 아닌데 형식이 비슷해서 오탐 |
| limitation_hard_negative | hardneg_0003 | 문서 버전은 sk-proj-example-not-real로 표시했습니다.  | 문서 버전은 <SECRET>로 표시했습니다.               | 실제 개인정보가 아닌데 형식이 비슷해서 오탐 |
| limitation_hard_negative | hardneg_0007 | 주문번호는 010-1234-5678-A입니다.                     | 주문번호는 <ACCOUNT_NUMBER>입니다.                 | 실제 개인정보가 아닌데 형식이 비슷해서 오탐 |
| limitation_adversarial   | adv_0001     | 주민번호는 900101 - 1234567 입니다.                   | 주민번호는 <ACCOUNT_NUMBER> 입니다.                | 변형된 입력에 대한 탐지 사례                |
| limitation_adversarial   | adv_0004     | 전화번호는 공일공-일이삼사-오육칠팔 입니다.           | 전화번호는 <PRIVATE_PERSON>                        | 변형된 입력에 대한 탐지 사례                |
| limitation_adversarial   | adv_0005     | API key는 sk-proj-abcDEF1234567890                    | API key는 <SECRET>                                 | 변형된 입력에 대한 탐지 사례                |
|                          |              | abcdef123456 입니다.                                  | abcdef123456 입니다.                               |                                             |