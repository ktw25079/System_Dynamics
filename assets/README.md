# 결과 그림

[torque_comparison.png](torque_comparison.png)는 같은 0–18.5 s 해석의 901개 저장 시각에서 토크 성분 선택을 수정하기 전후의 최대 절댓값을 비교합니다. 두 막대는 같은 N·m 축을 사용합니다. J2·J3·J4·J6은 TY에서 TZ로 변경했고 J1·J5는 TZ를 유지했습니다. 경로 변경이나 성능 향상을 비교한 그림이 아닙니다. [생성 코드](../scripts/plot_torque_comparison.py)

[fig04_final_task_layout.png](fig04_final_task_layout.png)는 스크류 집기 → 수직 배치 → 베어링 정렬 → 삽입·그리퍼 후퇴 순서를 보여 주는 설명용 이미지입니다.

주황색은 스크류, 청록색은 베어링, 파란색 화살표는 이동 방향을 나타냅니다. AI로 제작한 개념도로 실제 해석 캡처나 동작 영상이 아닙니다. 실제 모델 구성과 해석 조건은 [모델 설명](../docs/model.md)을 참고하세요.

`joint_torque.png`는 [보관 시계열](../results/torque_timeseries.csv)의 로컬 TZ 토크를 표시합니다. 여섯 패널은 각각 다른 세로축 범위를 사용하며, 점은 절댓값 최대 샘플입니다. [생성 코드](../scripts/plot_torque.py)

[프로젝트 개요](../README.md)
