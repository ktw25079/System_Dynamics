# 저장 결과 후처리

[postprocess_results.py](postprocess_results.py)는 저장된 RecurDyn Request를 읽어 관절 토크를 재계산합니다. **Python 3.10 이상, 표준 라이브러리만 사용**하며 RecurDyn을 실행하지 않습니다.

저장소 최상위에서 실행합니다.

```bash
# 저장 결과와 재계산 결과의 일치 여부만 검사
python scripts/postprocess_results.py --check

# results/의 CSV 두 개와 검증 JSON을 다시 생성
python scripts/postprocess_results.py

# 다른 입력·출력 경로 지정 옵션
python scripts/postprocess_results.py --help
```

| 기본 입력 | 역할 |
| --- | --- |
| [최종 RMD](../model/SystemDynamics_UR3_pick_place_screw_bearing.rmd) | 단위, 회전 조인트, I/J/RM 마커 연결 검사 |
| [보관 REQ](../results/solver/UR3_v81_clean_optimized.req) | 여섯 Request의 힘·모멘트와 901개 시각 |
| [joint_table.csv](../data/joint_table.csv) | 20개 모션 상태와 구간 평균 각속도 계산 |

스크립트는 0–18.5 s의 보관 실행을 대상으로 구성되어 있습니다. 다른 입력을 지정하더라도 샘플 수·모션 상태 수 등의 조건이 유지되는지 검사합니다.

[결과 파일](../results/README.md) · [계산 근거](../docs/torque_review.md) · [프로젝트 개요](../README.md)
