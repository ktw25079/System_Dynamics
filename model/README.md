# 최종 RecurDyn 모델

## 요구사항과 해결 방법

UR3가 스크류를 세워 놓고 베어링을 정렬해 삽입하도록 경로를 구성했습니다. 6개 회전 조인트에 STEP 모션을 적용하고, 강체 그리퍼·OnOff 구속으로 집기와 놓기를 표현했습니다. 마지막 베어링 하강에는 수직 가이드를 사용했습니다.

## 결과

20개 모션 상태로 18.5 s의 동작을 구성했습니다. 저장된 해석에서 관절별 901개 시각의 토크를 추출했습니다. [결과 확인](../results/README.md)

마찰 파지와 접촉 충격은 해석 범위에 포함하지 않았습니다.

## 파일과 실행

RecurDyn 2023에서 [주 모델](SystemDynamics_UR3_pick_place_screw_bearing.rdyn)을 엽니다. 아래 파일은 같은 폴더에 유지합니다.

| 파일 | 역할 |
| --- | --- |
| [모델 RDYN](SystemDynamics_UR3_pick_place_screw_bearing.rdyn) | UR3, 그리퍼, 스크류·베어링과 작업 환경 |
| [텍스트 모델 RMD](SystemDynamics_UR3_pick_place_screw_bearing.rmd) | 조인트·모션·Request 정의와 단위 확인 |
| [파라미터 RPP](SystemDynamics_UR3_pick_place_screw_bearing.rpp) | 두 작업물의 핵심 위치 파라미터 |
| [파라미터 RPV](SystemDynamics_UR3_pick_place_screw_bearing.rpv) | 최종 모델과 함께 보관한 PV 파일 |


[모델 구성](../docs/model.md) · [해석 설정과 실행](../docs/reproduction.md) · [프로젝트 개요](../README.md)
