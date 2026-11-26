# UR3 시뮬레이션 초기 정리본

[현재 포트폴리오 보기](https://github.com/ktw25079/System_Dynamics/tree/main)

이 브랜치는 파일별 커밋을 정리하기 전의 결과 보관본입니다. 학번이 포함된 보고서와 제공 CAD 형상이 포함된 RDYN은 별도 보관하고, 토크 재계산에 필요한 자료를 유지했습니다.

## 구현과 결과

스크류 이송·베어링 삽입을 20개 모션 상태, 18.5 s 경로로 구성한 RecurDyn 시뮬레이션입니다. 강체 그리퍼와 OnOff 구속을 사용하며 실제 마찰 파지·접촉 충격 시험은 포함하지 않습니다.

원시 해석의 0–18.5 s, 관절당 901개 저장 시각에서 로컬 TZ를 읽으면 J2의 샘플 최대 토크는 54.079 N·m입니다. 안전율 1.5 적용값은 81.119 N·m이며, 실제 모터 선정값과 구분합니다.

[모션·구속 정의](model/SystemDynamics_UR3_pick_place_screw_bearing.rmd) · [원시 Request](results/solver/UR3_v81_clean_optimized.req) · [결과 CSV](results/motor_capacity_summary.csv) · [후처리 코드](scripts/postprocess_results.py)

## 저장 결과 확인

저장소 최상위에서 Python 3.10 이상으로 실행합니다. 추가 패키지나 RecurDyn이 필요하지 않습니다.

```bash
python scripts/postprocess_results.py --check
```

[축 선택 근거](docs/torque_review.md) · [모델 구성](docs/model.md) · [원본 보유 시 해석 절차](docs/reproduction.md) · [정정 내역](docs/errata.md) · [자료 출처](docs/source_manifest.json)

RDYN을 포함하지 않으므로 이 브랜치만으로 원래 CAD 형상의 동작을 재생하거나 솔버를 재해석할 수는 없습니다.
