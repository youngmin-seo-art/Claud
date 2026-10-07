# [마스터 본보고서 제5장] 유무선 통합 HW·SW·네트워크·보안 상세 엔지니어링 설계

---

## 5.1. 산업용 RoIP 게이트웨이(ITS-GW100) 하드웨어 상세 사양 및 회로 설계

### 5.1.1. 하드웨어 블록 다이어그램 (Hardware Block Diagram)

`
> ITS-GW100 산업용 RoIP 게이트웨이 하드웨어 아키텍처
> [전원부 (Dual Redundant PSU)]
> • AC 100~240V 입력 ────┐
> • DC -48V 비상 입력 ───┴──> [전원 관리 PMIC] ──> 내부 DC 3.3V/1.8V/1.2V
> [메인 프로세서 서브시스템]
> • Quad-Core ARM Cortex-A53 1.5GHz Host SoC
> • 4GB LPDDR4 RAM + 32GB eMMC 5.1 Flash (OS & Local Buffer)
> • Dual 1Gbps Ethernet MAC + 2 x SFP Optical Interface
> [전용 DSP 오디오 프로세싱 서브시스템]
> • TI TMS320C6657 Dual-Core DSP (1.25GHz)
> • 8채널 하드웨어 오디오 코덱 (OPUS, AMR-WB, G.711, G.729)
> • Echo Cancellation (G.168 128ms) + AI Noise Suppressor
> [물리 인터페이스 보드 (8 Channel Isolated Analog Front-End)]
> • 8 x E&M Type I~V 오디오 트랜스포머 (600Ω Balanced, 1.5kV 격리)
> • 8 x Opto-coupler PTT 제어 입력 및 Relay PTT 출력
> • 4 x RS-232/422/485 직렬 제어 포트 (무전기 주파수 제어)
`

### 5.1.2. 전기적 및 기계적 상세 사양표

[표 5-1] ITS-GW100 세부 전기·기계 사양표

| 항목 | 상세 규격 및 시험 기준 |
| :--- | :--- |
| **섀시 규격** | 1U 19인치 표준 랙마운트 (482.6 x 44.5 x 280 mm) |
| **하우징 재질** | 고강도 알루미늄 아노다이징 (차폐 및 방열 설계) |
| **오디오 왜곡률** | THD+N < 0.05% @ 1kHz, 0dBm |
| **주파수 응답** | 200Hz ~ 3,400Hz (Narrowband) / 50Hz ~ 7,000Hz (Wide) |
| **PTT 지연시간** | 하드웨어 PTT 감지 및 SIP 패킷 생성 < 10ms |
| **코덱 트랜스코딩** | 지연시간 < 15ms (OPUS ↔ AMR-WB ↔ G.711) |
| **소비 전력** | 정격 25W (최대 부하 시 38W 이하) |
| **MTBF (평균수명)** | > 150,000 시간 (연속 가동 보장) |
| **내환경 시험** | 방진방수 IP54, 진동 MIL-STD-810G, 서지 보호 6kV |

---

## 5.2. AI 기반 지능형 재난 트래픽 우선순위 제어 엔진(AI-QoS) 알고리즘

### 5.2.1. 4계층 QCI/ARP 우선순위 매핑 모델
3GPP QoS Class Identifier(QCI) 및 Allocation and Retention Priority(ARP) 표준을 기반으로 재난 트래픽을 4계층으로 분류하고 선점형 스케줄링을 수행합니다.

[표 5-2] AI-QoS 4계층 트래픽 분류 및 스케줄링 매트릭스

| Class | 트래픽 유형 | QCI | ARP | 보장 지연 | 선점(Preemption) 정책 |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **Class 1** | 긴급 인명구조 음성<br>(MCPTT Emergency) | 65 | 1 | < 75 ms | 선점 불가 (최우선 보장)<br>• 타 트래픽 강제 자원 해제 |
| **Class 2** | 현장 지휘관 지령 및 긴급 다자간 화상회의 음성/시그널링 | 66/69 | 2 | < 100 ms | Class 3/4 선점 가능 |
| **Class 3** | 다자간 재난 화상회의 영상 (H.323/WebRTC/MCVideo) & CCTV | 67 | 8 | < 200 ms | 네트워크 포화 시 비트레이트 50% 자동 감축 및 적응형 코덱 전환 |
| **Class 4** | 일반 행정 데이터 / 파일 전송 / 시스템 로그 | 69-Def | 15 | Best Effort | 대역폭 차단/지연 (Buffer Drop 허용) |

### 5.2.2. 강화학습 기반 동적 대역폭 할당 알고리즘 (DRL-QoS)
네트워크 상태 $S_t = (\text{Bandwidth}, \text{Packet Loss}, \text{Latency}, \text{Queue Length})$에 대해 인공신경망 정책 $\pi_\theta(a|s)$가 최적의 대역폭 할당 행동 $a_t$를 결정합니다:

$$\max_\theta \mathbb{E} \left[ \sum_{t=0}^T \gamma^t \cdot \left( R_{\text{voice}} - \alpha \cdot \text{Loss}_{\text{voice}} - \beta \cdot \text{Delay}_{\text{video}} \right) \right]$$

---

## 5.3. 위치기반 자동 그룹 바인딩(AGB, Auto Group Binding) 엔진 설계

[표 5-3] 위치기반 자동 그룹 바인딩(AGB) 단계별 처리 흐름

| 처리 단계 | AGB 엔진 세부 동작 알고리즘 | 소요 시간 | 연계 서브시스템 |
|---|---|---|---|
| **1. 이벤트 감지** | 유선 IP 비상벨 푸시 또는 119/112 CTI 신고 데이터베이스 트리거 수신 | 즉시 (10ms) | IP 비상벨 / 119·112 CTI |
| **2. 위치 좌표 추출** | 신고 지점의 GPS 위경도(Lat, Lon) 및 실내 공간 번호(Indoor Map ID) 파싱 | 20ms | GIS 지리정보 데이터베이스 |
| **3. 공간 인덱싱 검색** | 2D/3D Spatial R-Tree 인덱스를 가동하여 사고 지점 기준 반경 $R$ (도심 500m, 농어촌 2km) 내 단말 검색 | 80ms | GIS 공간 분석 서버 |
| **4. 현장 자원 식별** | 반경 내 위치한 현장 소방관 단말, 경찰 순찰차 단말, 지자체 당직 관제 PC 목록 실시간 추출 | 50ms | MCPTT HSS 단말 위치 DB |
| **5. 동적 토크그룹/화상 세션 생성** | SIP Core에서 임시 비상 통화그룹 ID 및 다자간 긴급 화상회의 세션 ID 동적 프로비저닝 | 120ms | 3GPP MCPTT/MCVideo Core 서버 |
| **6. 일제 호 호출 & 화상 팝업** | 식별된 단말로 병렬 SIP INVITE 송출, 단말 스피커폰 강제 개방 및 지자체장·지휘관 화상회의실 화면에 현장 영상 자동 팝업 | 500ms | RoIP/Video 게이트웨이 및 LTE 기지국 |
| **종합 성능** | **신고 접수부터 다부처 현장 요원 동시 통화 및 지휘관 화상회의 개시까지 총 소요 시간** | **총 780ms** | **1초 이내 (골든타임 선점 달성)** |

- **성능 벤치마크:** 반경 내 200개 단말 및 화상회의 세션 바인딩 완료 시간 **780ms (1초 미만 달성)**.

---

## 5.4. KCMVP 암호화 및 국가 공공망 보안/망분리 연계 아키텍처

[표 5-4] KCMVP 암호화 및 계층별 보안 아키텍처 규격

| 보안 계층 | 적용 보안 기술 및 암호화 알고리즘 | 국가 인증 기준 및 보안 규격 | 망분리 및 접근제어 메커니즘 |
|---|---|---|---|
| **지자체 폐쇄망 & 화상망 연동** | KCMVP 검증필 ARIA-256 / LEA 하드웨어 암호화 칩셋, TLS 1.3 / SRTP | 국가정보원 KCMVP 보안 2등급 이상 인증 | 지자체 CCTV VMS 및 정부 화상회의망과 재난통신망 간 물리적/논리적 1방향(Data Diode) 연동 게이트웨이 |
| **백본 전송 구간 암호화** | IPSec VPN 터널링 (RFC 4301, IKEv2, AES-GCM-256) | 전자정부 공공망 보안 가이드라인 준수 | 통신사업자 임차 백본 상에서 엔드-투-엔드(E2E) 전용 암호화 터널 구축 (도청/변조 100% 차단) |
| **코어망 침입 방지 & 감시** | 차세대 AI 기반 비정상 트래픽 탐지기 & IPS (24/7 가동) | CC EAL4+ 인증 전산망 방화벽 체계 | 초당 100만 패킷(Mpps) 수준의 DDoS 및 비인가 SIP INVITE 플러딩 실시간 자동 차단 |
