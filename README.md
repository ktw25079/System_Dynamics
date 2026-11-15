# UR3 Pick & Place

**6축 UR3의 스크류 이송·베어링 삽입을 모델링하고, 저장된 해석 결과로 관절 토크를 검토한 프로젝트.**

2026년 1학기 시스템동역학 · 강태욱 · RecurDyn 2023

[최종 모델](model/README.md) · [실행 안내](docs/reproduction.md) · [검증 결과](results/README.md) · [설계 문서](docs/README.md)

## 목적

UR3가 스크류를 목표 위치에 세운 뒤, 베어링을 이송해 스크류에 수직으로 끼우는 시뮬레이션입니다. CAD 기반 동역학 모델링부터 경로 설정, 관절 토크 분석까지의 결과를 정리했습니다.

![UR3의 스크류 집기, 배치, 베어링 정렬 및 삽입 순서](assets/fig04_final_task_layout.png)

<sub>스크류 이송과 베어링 삽입 순서 개념도</sub>

## 진행 과정

CAD 형상으로 6축 로봇과 작업물을 구성하고, 웨이포인트와 조인트 모션을 설정한 뒤 해석 결과에서 관절별 토크를 계산했습니다.

### 작업 순서

| 단계 | 수행 동작 |
|:---:|---|
| **01 · Pick** | 스크류에 접근하여 집고 들어 올립니다. |
| **02 · Place** | 스크류를 목표 위치로 옮겨 수직으로 배치합니다. |
| **03 · Align** | 홀더의 베어링을 집어 스크류 상부에 동축으로 정렬합니다. |
| **04 · Insert** | 베어링을 수직으로 삽입하고 그리퍼를 후퇴시킵니다. |

두 물체에 각각 **5개의 핵심 웨이포인트**를 지정했으며, 총 **20개 모션 상태**로 **18.5초**의 작업을 구성했습니다.

## 주요 결과

**18.5 s 작업 · 관절당 901개 샘플.** 저장된 Request의 로컬 회전축 **TZ**에서 구한 절댓값 최대 토크입니다(N·mm → N·m). [계산 기록](results/verification.json)

| 관절 | 최대 토크 (N·m) | 안전율 1.5 적용 (N·m) |
|---|---:|---:|
| J1 · Base | 6.461 | 9.691 |
| J2 · Shoulder | 54.079 | 81.119 |
| J3 · Elbow | 21.968 | 32.953 |
| J4 · Wrist 1 | 15.211 | 22.817 |
| J5 · Wrist 2 | 6.642 | 9.963 |
| J6 · Wrist 3 | 0.120 | 0.180 |

**J2가 가장 큰 관절 토크를 요구합니다.** 실제 모터 선정에는 감속비, 효율, 속도 및 RMS 토크를 추가로 고려해야 합니다. [계산 근거](docs/torque_review.md) · [결과 CSV](results/motor_capacity_summary.csv)

## 파일 안내

| 경로 | 내용 |
|---|---|
| [model/](model/README.md) | 최종 RecurDyn 모델과 해석·파라미터 파일 |
| [data/](data/README.md) | 웨이포인트, 관절 자세, 기하학적 여유 검토 |
| [results/](results/README.md) | 수정된 토크 결과와 최종 솔버 원시 데이터 |
| [scripts/](scripts/README.md) | 토크 재계산 및 결과 검증 스크립트 |
| [docs/](docs/README.md) | 과제 요구사항, 모델 구성, 재현 절차와 정정 내역 |
| [reports/](reports/README.md) | 기존 과제 보고서 PDF·DOCX와 현재 결과의 차이 |
| [assets/](assets/README.md) | 작업 순서 개념도 |

## 실행 방법

1. 저장소를 내려받고 RecurDyn 2023에서 [최종 `.rdyn` 모델](model/SystemDynamics_UR3_pick_place_screw_bearing.rdyn)을 엽니다.
2. 작업 사본을 저장한 뒤 **Dynamic Analysis**를 **18.5 s**까지 실행합니다.
3. 애니메이션과 `REQ_TORQUE_J1`–`REQ_TORQUE_J6` 결과를 확인합니다.

`model/`의 `.rmd`, `.rpp`, `.rpv` 파일을 함께 보관하세요. 단위와 적분기 설정, 단계별 시각은 [재현 절차](docs/reproduction.md)에 정리했습니다.

저장된 해석 결과의 일치 여부는 **Python 3.10 이상**에서 확인합니다. 추가 패키지나 RecurDyn 실행이 필요하지 않습니다.

```bash
git clone https://github.com/ktw25079/System_Dynamics.git
cd System_Dynamics
python scripts/postprocess_results.py --check
```

결과 파일을 다시 만들려면 `python scripts/postprocess_results.py`를 실행합니다. [입력·출력과 검사 항목](scripts/README.md)

## 모델링 범위

6개 회전 조인트에 STEP 모션을 적용하고, 단일 강체 그리퍼와 OnOff 구속 전환으로 물체를 이송합니다. 베어링의 마지막 하강은 수직 가이드로 제어합니다. 실제 마찰 파지, 자유낙하, 접촉 충격 및 PID 제어는 포함하지 않습니다.

기존 보고서와 최종 모델의 차이, 토크 축 수정 근거는 [정정 내역](docs/errata.md)에 정리했습니다.

[과제 요구사항](docs/requirements.md) · [자료 출처](docs/source_manifest.json)
