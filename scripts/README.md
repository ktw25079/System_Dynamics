# 저장 결과 후처리

[postprocess_results.py](postprocess_results.py)는 저장된 RecurDyn Request를 읽어 관절 토크를 재계산합니다. **Python 3.10 이상, 표준 라이브러리만 사용**하며 RecurDyn을 실행하지 않습니다.

모멘트 합력 대신 조인트의 로컬 회전축 성분을 선택하기 위해 RMD의 I/J/RM 마커 연결과 단위를 검사합니다. REQ의 901개 시각을 읽어 N·mm를 N·m로 환산하고, 관절별 최대 토크·발생 시각·안전율 적용값을 계산합니다.

결과는 [토크 시계열](../results/torque_timeseries.csv), [용량 요약](../results/motor_capacity_summary.csv), [검증 JSON](../results/verification.json)으로 저장합니다. 보관 실행의 J2 최대 토크는 **54.079 N·m**입니다.

## 실행 방법

저장소 최상위에서 실행합니다.

```bash
# 저장 결과와 재계산 결과의 일치 여부만 검사
python3 scripts/postprocess_results.py --check

# results/의 CSV 두 개와 검증 JSON을 다시 생성
python3 scripts/postprocess_results.py

# 다른 입력·출력 경로 지정 옵션
python3 scripts/postprocess_results.py --help
```

| 기본 입력 | 역할 |
| --- | --- |
| [최종 RMD](../model/SystemDynamics_UR3_pick_place_screw_bearing.rmd) | 단위, 회전 조인트, I/J/RM 마커 연결 검사 |
| [보관 REQ](../results/solver/UR3_v81_clean_optimized.req) | 여섯 Request의 힘·모멘트와 901개 시각 |
| [joint_table.csv](../data/joint_table.csv) | 20개 모션 상태와 구간 평균 각속도 계산 |

스크립트는 0–18.5 s의 보관 실행을 대상으로 구성되어 있습니다. 다른 입력을 지정하더라도 샘플 수·모션 상태 수 등의 조건이 유지되는지 검사합니다.

[결과 파일](../results/README.md) · [계산 근거](../docs/torque_review.md) · [프로젝트 개요](../README.md)

## 토크 그래프

[plot_torque.py](plot_torque.py)는 보관 CSV에서 여섯 관절의 토크 그림을 생성합니다. 그래프 생성에만 Matplotlib이 필요하며 기존 결과 검사는 표준 라이브러리만 사용합니다.

```bash
python3 -m pip install matplotlib
python3 scripts/plot_torque.py
python3 scripts/plot_torque_comparison.py
```

[plot_torque_comparison.py](plot_torque_comparison.py)는 [정정 전 요약](../data/original/motor_capacity_summary.csv)과 [현재 요약](../results/motor_capacity_summary.csv)을 같은 N·m 축에서 비교해 [README 대표 그래프](../assets/torque_comparison.png)를 만듭니다. 동일 해석의 성분 선택 정정이며, 시뮬레이션 성능 개선을 비교하지 않습니다. Windows에서는 설치된 명령에 따라 `python3` 대신 `python`을 사용합니다.
