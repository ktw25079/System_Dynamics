# 경로와 기하 검토 데이터

| 파일 | 내용 | 사용 기준 |
| --- | --- | --- |
| [pp_waypoints.csv](pp_waypoints.csv) | 스크류·베어링 각각 5개 핵심 위치 | 작업 경로 설명 |
| [joint_table.csv](joint_table.csv) | 20개 모션 상태의 시각·조인트 각도 | 후처리 입력, 시각 s·각도 deg |
| [clearance_audit.csv](clearance_audit.csv) | 지정 형상·목표 위치의 여유 검토 | 전 경로 충돌 검사와 구분 |
| [original/](original/) | 정정 전 토크 시계열·용량 요약 | 이력 보존용, 현재 결과는 아래 링크 사용 |

CSV의 위치를 고치는 것만으로 모델의 STEP 모션이 자동 갱신되지는 않습니다. 최종 모델과 입력의 관계는 [모델 구성](../docs/model.md)을 참고하세요.

[현재 토크 결과](../results/README.md) · [정정 내역](../docs/errata.md) · [프로젝트 개요](../README.md)
