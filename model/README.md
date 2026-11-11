# 최종 RecurDyn 모델

RecurDyn 2023에서 [주 모델](SystemDynamics_UR3_pick_place_screw_bearing.rdyn)을 엽니다. 아래 파일은 같은 폴더에 유지합니다.

| 파일 | 역할 |
| --- | --- |
| [모델 RDYN](SystemDynamics_UR3_pick_place_screw_bearing.rdyn) | UR3, 그리퍼, 스크류·베어링과 작업 환경 |
| [텍스트 모델 RMD](SystemDynamics_UR3_pick_place_screw_bearing.rmd) | 조인트·모션·Request 정의와 단위 확인 |
| [파라미터 RPP](SystemDynamics_UR3_pick_place_screw_bearing.rpp) | 두 작업물의 핵심 위치 파라미터 |
| [파라미터 RPV](SystemDynamics_UR3_pick_place_screw_bearing.rpv) | 최종 모델과 함께 보관한 PV 파일 |

6개 회전 조인트에 STEP 모션을 적용합니다. 집기·놓기는 강체 그리퍼와 OnOff 구속, 마지막 베어링 하강은 수직 가이드로 표현합니다. 실제 마찰 파지나 접촉 충격을 해석하는 모델은 아닙니다.

[모델 구성](../docs/model.md) · [해석 설정과 실행](../docs/reproduction.md) · [프로젝트 개요](../README.md)
