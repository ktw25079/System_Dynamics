# 관절 토크와 검증 결과

관절별 구동 토크를 구하기 위해 **0–18.5 s, 관절당 901개 저장 시각**을 기준으로 여섯 회전 조인트의 로컬 TZ를 읽고 N·mm에서 N·m로 환산한 결과입니다. J2의 샘플 절댓값 최대 토크는 **54.079 N·m**, 안전율 1.5 적용값은 **81.119 N·m**입니다.

| 파일 | 내용 |
| --- | --- |
| [motor_capacity_summary.csv](motor_capacity_summary.csv) | 관절별 최대 토크·발생 시각·안전율 적용값 |
| [torque_timeseries.csv](torque_timeseries.csv) | 시각별 로컬 회전축 토크와 힘·모멘트 합력 |
| [verification.json](verification.json) | 단위·샘플 수·입력 SHA-256·해석 한계 |
| [solver/](solver/) | 기존 최종 실행의 REQ·RMD·RAN·RAD·RPLT 원시 파일 |

## 저장 결과 확인

저장소 최상위에서 실행합니다. 파일을 덮어쓰거나 솔버를 실행하지 않습니다.

```bash
python3 scripts/postprocess_results.py --check
```

최대 토크는 저장 시각의 샘플 최대값입니다. 실제 모터 축 요구 토크와 같지 않으며, 모터 선정에는 감속비·효율·속도·RMS 토크 검토가 추가로 필요합니다.

이전 보고서의 J2·J3·J4·J6 값은 다른 축 성분을 사용했습니다. [축 선택 근거](../docs/torque_review.md) · [정정 내역](../docs/errata.md)

[프로젝트 개요](../README.md)
