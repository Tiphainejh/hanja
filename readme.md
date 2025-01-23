# Hanja getter for korean
Check the code documentation here : https://tiphainejh.github.io/hanja/

# TODO
- [x] Add function to fetch data from DB even when there is no associated hanja
- [x] Fix the width of the container
- [x] Change that the color hover is only when the div isnt collapsed
- [x] Change the definitions position
- [ ] Add functionality to search korean text even if its not full
- [x] Check responsive design for phones 
- [ ] Add audio and other values to the DB
- [ ] Change Doxygen Css https://codepen.io/havardob/pen/PopKJRE 

### 1. **Creation of the database**

- **Data collection**: Korean dictionary obtained from https://krdict.korean.go.kr/download/downloadPopup and hanja obtained from https://github.com/myungcheol/hanja.
- **Data structure**: Two databases created with sqlite3. Diagram generated with DBeaver.

### 2. **Development of an association algorithm**

- **Morphological analysis**: Develop a tool that breaks down Korean words into their hanja components. This may involve the use of specialized natural language processing (NLP) libraries for Korean.
- **Word association**: Once the hanja have been identified for a given word, search for all the other words that share these same characters. You can create indexes or relationship tables to make this search easier.

### 3. **User Interface Design**

- **Web or mobile application**: Determine the platform best suited to your needs. A web app would be accessible from any device, while a mobile app could offer a more personalized experience.
- **Key Features**:
  - **Korean word entry**: Allow the user to enter the word they want to study.
  - **Display of corresponding hanja**: Show the hanja characters associated with the entered word.
  - **List of related words**: Display a list of words that contain the same hanja, with their definitions and examples.
  - **Favorites and Notes**: Allow the user to save words and add annotations for easy revision later.

### 4. **Improved user experience**

- **Graphical visualization**: Integrate graphics or mind maps to visually represent the links between words and their Hanja roots.
- **Advanced search**: Add filters to sort words by frequency of use, language level (formal/informal), or field (scientific, literary, etc.).
- **Fonts**: Korean title : https://noonnu.cc/font_page/1100; English title : https://bboxtype.com/typefaces/FFF_tuoi_tre/, https://dirtylinestudio.com/product/neue-metana-next-free-font/

### 5. **Later improvements**

- **Dictionnary API** : https://opendict.korean.go.kr/service/openApiInfo 

# Brainstorming ideas for name

- 언어의 뿌리 (Eoneoui Ppuri: "Roots of Language").
- 배움의 연결 (Baeum-ui Yeongyeol: "Connections of Learning").
- 한자풀 (Hanja Pul: "Hanja Unraveled").
- 뿌리와 말 (Ppuri wa Mal: "Roots and Words"). 
 
# Notes

- 출당

<details>
  <summary>For test purposes, words that have hanja that aren't contained in any other words :
  </summary>
Word: 쾌재, Hanja: 哉    
Word: 쾌청하다, Hanja: 晴
Word: 타액, Hanja: 唾    
Word: 탈구, Hanja: 臼    
Word: 태권도, Hanja: 跆  
Word: 태풍, Hanja: 颱    
Word: 토사곽란, Hanja: 癨
Word: 토사구팽, Hanja: 兔
Word: 파초, Hanja: 芭
Word: 파초, Hanja: 蕉
Word: 파충류, Hanja: 爬
Word: 판공비, Hanja: 辦
Word: 판막, Hanja: 瓣
Word: 패물, Hanja: 佩
Word: 편린, Hanja: 鱗
Word: 폄하하다, Hanja: 貶
Word: 폐백, Hanja: 帛
Word: 폐하, Hanja: 陛
Word: 폐허, Hanja: 墟
Word: 포로, Hanja: 虜
Word: 표범, Hanja: 豹
Word: 표주박, Hanja: 瓢
Word: 풍미하다, Hanja: 靡
Word: 피폭, Hanja: 曝
Word: 필, Hanja: 疋
Word: 필경, Hanja: 竟
Word: 하수구, Hanja: 溝
Word: 하자, Hanja: 瑕
Word: 하자, Hanja: 疵
Word: 학질, Hanja: 瘧
Word: 한라산, Hanja: 拏
Word: 함정, Hanja: 穽
Word: 함정, Hanja: 檻
Word: 항간, Hanja: 巷
Word: 항문, Hanja: 肛
Word: 해당화, Hanja: 棠
Word: 해태, Hanja: 獬
Word: 해태, Hanja: 豸
Word: 현란하다, Hanja: 絢
Word: 혈혈단신, Hanja: 孑
Word: 혜성, Hanja: 彗
Word: 호구, Hanja: 餬
Word: 호반, Hanja: 畔
Word: 호호백발, Hanja: 皜
Word: 혼쭐, Hanja: 쭐
Word: 홈통, Hanja: 홈
Word: 홍어, Hanja: 䱋
Word: 홍채, Hanja: 虹
Word: 홍합, Hanja: 蛤
Word: 화강암, Hanja: 崗
Word: 화기애애하다, Hanja: 靄
Word: 화류계, Hanja: 柳
Word: 화훼, Hanja: 卉
Word: 환관, Hanja: 宦
Word: 황달, Hanja: 疸
Word: 황당무계하다, Hanja: 稽
Word: 황무지, Hanja: 蕪
Word: 회충, Hanja: 蛔
Word: 회화, Hanja: 繪
Word: 횡격막, Hanja: 膈
Word: 효시, Hanja: 嚆
Word: 효시, Hanja: 矢
Word: 후각, Hanja: 嗅
Word: 후사, Hanja: 嗣
Word: 흉금, Hanja: 襟
Word: 희열, Hanja: 悅
Word: 희한하다, Hanja: 罕
Word: 희화적, Hanja: 戱
Word: 가부좌, Hanja: 跏
Word: 가부좌, Hanja: 趺
Word: 가상하다, Hanja: 嘉
Word: 간극, Hanja: 隙
Word: 간석지, Hanja: 潟
Word: 간신히, Hanja: 艱
Word: 감질나다, Hanja: 疳
Word: 갑각류, Hanja: 殼
Word: 갑갑증, Hanja: 갑
Word: 갑론을박, Hanja: 乙
Word: 갑주, Hanja: 胄
Word: 강경하다, Hanja: 勁
Word: 강보, Hanja: 襁
Word: 강시, Hanja: 僵
Word: 강시, Hanja: 殭
Word: 강태공, Hanja: 姜
Word: 개전, Hanja: 悛
Word: 거절당하다, Hanja: 絶
Word: 거치, Hanja: 据
Word: 건곤, Hanja: 坤
Word: 견갑골, Hanja: 胛
Word: 견사, Hanja: 繭
Word: 견훤, Hanja: 甄
Word: 견훤, Hanja: 萱
Word: 겸연스레, Hanja: 歉
Word: 경기도, Hanja: 畿
Word: 경륜, Hanja: 綸
Word: 경운기, Hanja: 耘
Word: 경위, Hanja: 涇
Word: 경위, Hanja: 渭
Word: 경추, Hanja: 頸
Word: 경치다, Hanja: 黥
Word: 경혈, Hanja: 穴
Word: 경희궁, Hanja: 熙
Word: 계제, Hanja: 梯
Word: 고량주, Hanja: 粱
Word: 고봉, Hanja: 捧
Word: 고혹적, Hanja: 蠱
Word: 고환, Hanja: 睾
Word: 골격, Hanja: 骼
Word: 공복, Hanja: 僕
Word: 공비, Hanja: 匪
Word: 곶, Hanja: 串
Word: 관아, Hanja: 衙
Word: 광야, Hanja: 曠
Word: 괴뢰군, Hanja: 傀
Word: 괴뢰군, Hanja: 儡
Word: 굉음, Hanja: 轟
Word: 교량, Hanja: 梁
Word: 교목, Hanja: 喬
Word: 교편, Hanja: 鞭
Word: 구가하다, Hanja: 謳
Word: 구강, Hanja: 腔
Word: 구기자, Hanja: 枸
Word: 구미호, Hanja: 狐
Word: 구절판, Hanja: 坂
Word: 구제역, Hanja: 蹄
Word: 군색하다, Hanja: 窘
Word: 궤변, Hanja: 詭
Word: 규수, Hanja: 閨
Word: 규장각, Hanja: 奎
Word: 근저, Hanja: 柢
Word: 금고형, Hanja: 錮
Word: 금괴, Hanja: 塊
Word: 금수, Hanja: 禽
Word: 급거, Hanja: 遽
Word: 급기야, Hanja: 也
Word: 긍휼, Hanja: 恤
Word: 기구하다, Hanja: 崎
Word: 기구하다, Hanja: 嶇
Word: 기근, Hanja: 饉
Word: 기라성, Hanja: 綺
Word: 기량, Hanja: 倆
Word: 기량, Hanja: 伎
Word: 기린, Hanja: 麒
Word: 기린, Hanja: 麟
Word: 기치, Hanja: 幟
Word: 나무아미타불, Hanja: 陀
Word: 나약하다, Hanja: 愞
Word: 나전 칠기, Hanja: 鈿
Word: 나졸, Hanja: 邏
Word: 낙동강, Hanja: 洛
Word: 낙타, Hanja: 駱
Word: 낙타, Hanja: 駞
Word: 난간, Hanja: 杆
Word: 난삽하다, Hanja: 澁
Word: 낭자, Hanja: 娘
Word: 노, Hanja: 櫓
Word: 노비, Hanja: 婢
Word: 노회하다, Hanja: 獪
Word: 녹록하다, Hanja: 碌
Word: 녹용, Hanja: 茸
Word: 농아, Hanja: 聾
Word: 늠름하다, Hanja: 凜
Word: 능가하다, Hanja: 駕
Word: 능선, Hanja: 稜
Word: 다마네기, Hanja: 葱
Word: 담, Hanja: 痰
Word: 담장, Hanja: 牆
Word: 대구, Hanja: 邱
Word: 대금, Hanja: 笒
Word: 대종교, Hanja: 倧
Word: 대지, Hanja: 垈
Word: 대퇴부, Hanja: 腿
Word: 대화재, Hanja:
Word: 도서, Hanja: 嶼
Word: 도정하다, Hanja: 搗
Word: 도포, Hanja: 袍
Word: 돈가스, Hanja: 豚
Word: 동백, Hanja: 栢
Word: 동서, Hanja: 壻
Word: 동체, Hanja: 胴
Word: 동통, Hanja: 疼
Word: 두견새, Hanja: 鵑
Word: 둔부, Hanja: 臀
Word: 리, Hanja: 釐
Word: 리, Hanja: 厘
Word: 마, Hanja: 碼
Word: 마구간, Hanja: 廏
Word: 마마, Hanja: 媽
Word: 망종, Hanja: 芒
Word: 매연, Hanja: 煤
Word: 면, Hanja: 麪
Word: 명석하다, Hanja: 晳
Word: 명징하다, Hanja: 澄
Word: 모과, Hanja: 瓜
Word: 목도하다, Hanja: 睹
Word: 목탁, Hanja: 鐸
Word: 몽롱하다, Hanja: 朦
Word: 몽롱하다, Hanja: 朧
Word: 무도회, Hanja: 蹈
Word: 무희, Hanja: 姬
Word: 문지방, Hanja: 枋
Word: 물론, Hanja: 勿
Word: 미륵, Hanja: 勒
Word: 미제, Hanja: 謎
Word: 밀랍, Hanja: 蠟
Word: 반석, Hanja: 磐
Word: 반창고, Hanja: 絆
Word: 발인, Hanja: 靷
Word: 발해, Hanja: 渤
Word: 방광, Hanja: 膀
Word: 방광, Hanja: 胱
Word: 방대하다, Hanja: 厖
Word: 방대하다, Hanja: 尨
Word: 방불하다, Hanja: 彿
Word: 방불하다, Hanja: 髣
Word: 방불하다, Hanja: 髴
Word: 방패, Hanja: 旁
Word: 백로, Hanja: 鷺
Word: 백태, Hanja: 苔
Word: 번째, Hanja: 째
Word: 범주, Hanja: 疇
Word: 벽두, Hanja: 劈
Word: 변발, Hanja: 辮
Word: 별안간, Hanja: 瞥
Word: 별주부전, Hanja: 鼈
Word: 병풍, Hanja: 屛
Word: 보모, Hanja: 姆
Word: 보살, Hanja: 菩
Word: 보살, Hanja: 薩
Word: 보우하다, Hanja: 佑
Word: 복채, Hanja: 卜
Word: 볼연지, Hanja: 臙
Word: 부마, Hanja: 駙
Word: 부산, Hanja: 釜
Word: 부평초, Hanja: 萍
Word: 북망산, Hanja: 邙
Word: 분위기, Hanja: 雰
Word: 비단, Hanja: 緋
Word: 비등하다, Hanja: 沸
Word: 비밀번호, Hanja: 秘
Word: 비위, Hanja: 脾
Word: 비파, Hanja: 琵
Word: 비파, Hanja: 琶
Word: 빈사, Hanja: 瀕
Word: 빈소, Hanja: 殯
Word: 빈축, Hanja: 嚬
Word: 빈축, Hanja: 蹙
Word: 빈축, Hanja: 顰
Word: 사당, Hanja: 祠
Word: 사소하다, Hanja: 些
Word: 사이비, Hanja: 而
Word: 사지, Hanja: 肢
Word: 사직, Hanja: 稷
Word: 삼고초려, Hanja: 廬
Word: 삼파전, Hanja: 巴
Word: 삽시간, Hanja: 霎
Word: 상서롭다, Hanja: 瑞
Word: 생질, Hanja: 甥
Word: 서광, Hanja: 曙
Word: 서설, Hanja: 絮
Word: 서한, Hanja: 翰
Word: 석가모니, Hanja: 尼
Word: 선박, Hanja: 舶
Word: 선비, Hanja: 妣
Word: 선영, Hanja: 塋
Word: 설탕, Hanja: 屑
Word: 섬광, Hanja: 閃
Word: 섬진강, Hanja: 蟾
Word: 성황당, Hanja: 隍
Word: 소풍, Hanja: 逍
Word: 소화전, Hanja: 栓
Word: 송골매, Hanja: 鶻
Word: 송연하다, Hanja: 竦
Word: 송편, Hanja: 편
Word: 수달, Hanja: 㺚
Word: 수전증, Hanja: 顫
Word: 수척하다, Hanja: 瘦
Word: 수포, Hanja: 疱
Word: 수효, Hanja: 爻
Word: 숙맥, Hanja: 菽
Word: 숙원, Hanja: 夙
Word: 순, Hanja: 笋
Word: 순록, Hanja: 馴
Word: 순박하다, Hanja: 淳
Word: 슬하, Hanja: 膝
Word: 시추, Hanja: 錐
Word: 식이 요법, Hanja: 餌
Word: 식혜, Hanja: 醯
Word: 신기루, Hanja: 蜃
Word: 신병, Hanja: 柄
Word: 신음, Hanja: 呻
Word: 싫증, Hanja: 싫
Word: 십계명, Hanja: 誡
Word: 십시일반, Hanja: 匙
Word: 싸전, Hanja: 廛
Word: 아령, Hanja: 鈴
Word: 아쟁, Hanja: 箏
Word: 아킬레스건, Hanja: 腱
Word: 아편, Hanja: 鴉
Word: 아홉수, Hanja: 홉
Word: 악어, Hanja: 鰐
Word: 안장, Hanja: 鞍
Word: -암, Hanja: 菴
Word: 압록강, Hanja: 鴨
Word: 압정, Hanja: 釘
Word: 애로, Hanja: 隘
Word: 액취증, Hanja: 腋
Word: 앵무새, Hanja: 鵡
Word: 양말, Hanja: 襪
Word: 양말, Hanja: 韈
Word: 양송이, Hanja: 栮
Word: 양악, Hanja: 顎
Word: 양조, Hanja: 釀
Word: 어패류, Hanja: 貝
Word: 억측, Hanja: 臆
Word: 엔, Hanja: 円
Word: 여명, Hanja: 黎
Word: 역시, Hanja: 亦
Word: 연미복, Hanja: 燕
Word: 연민, Hanja: 愍
Word: 연어, Hanja: 鰱
Word: 연필심, Hanja: 芯
Word: 영리하다, Hanja: 怜
Word: 영리하다, Hanja: 悧
Word: 영리하다, Hanja: 伶
Word: 영리하다, Hanja: 俐
Word: 영아, Hanja: 嬰
Word: 영지, Hanja: 芝
Word: 오류, Hanja: 謬
Word: 옥새, Hanja: 璽
Word: 온돌, Hanja: 堗
Word: 와사비, Hanja: 葵
Word: 와신상담, Hanja: 薪
Word: 와신상담, Hanja: 嘗
Word: 와중, Hanja: 渦
Word: 완두콩, Hanja: 豌
Word: 왕림하다, Hanja: 枉
Word: 요람, Hanja: 籃
Word: 요원하다, Hanja: 遙
Word: 요원하다, Hanja: 遼
Word: 요조숙녀, Hanja: 窈
Word: 요조숙녀, Hanja: 窕
Word: 요지경, Hanja: 瑤
Word: 요철, Hanja: 凹
Word: 요철, Hanja: 凸
Word: 요통, Hanja: 腰
Word: 욕창, Hanja: 褥
Word: 우동, Hanja: 饂
Word: 우동, Hanja: 飩
Word: 우화, Hanja: 寓
Word: 운석, Hanja: 隕
Word: 울산, Hanja: 蔚
Word: 웅담, Hanja: 熊
Word: 원둘레, Hanja: 둘
Word: 원삼, Hanja: 衫
Word: 원앙금침, Hanja: 衾
Word: 유언비어, Hanja: 蜚
Word: 유화, Hanja: 宥
Word: 윤락, Hanja: 淪
Word: 융단, Hanja: 絨
Word: 의장대, Hanja: 仗
Word: 이, Hanja: 貳
Word: 이앙기, Hanja: 秧
Word: 이율곡, Hanja: 栗
Word: 이이, Hanja: 珥
Word: 이재민, Hanja: 罹
Word: 이질, Hanja: 痢
Word: 이황, Hanja: 滉
Word: 익일, Hanja: 翌
Word: 일, Hanja: 壹
Word: 일엽편주, Hanja: 舟
Word: 일확천금, Hanja: 攫
Word: 자양분, Hanja: 滋
Word: 잔재, Hanja: 滓
Word: 잠언, Hanja: 箴
Word: 재앙, Hanja: 殃
Word: 재원, Hanja: 媛
Word: 재취, Hanja: 娶
Word: 저돌적, Hanja: 豬
Word: 전갈, Hanja: 蠍
Word: 전당포, Hanja: 舖
Word: 전대, Hanja: 纏
Word: 전몰, Hanja: 歿
Word: 전복, Hanja: 鰒
Word: 전철, Hanja: 轍
Word: 전형, Hanja: 銓
Word: 접영, Hanja: 蝶
Word: 정곡, Hanja: 鵠
Word: 정녕, Hanja: 叮
Word: 정문, Hanja: 旌
Word: 정승, Hanja: 丞
Word: 정신대, Hanja: 挺
Word: 정화, Hanja: 菁
Word: 젖병, Hanja: 젖
Word: 제후, Hanja: 侯
Word: 젬병, Hanja: 젬
Word: 조강지처, Hanja: 糟
Word: 조강지처, Hanja: 糠
Word: 조세, Hanja: 租
Word: 조예, Hanja: 詣
Word: 조짐, Hanja: 朕
Word: 조타실, Hanja: 舵
Word: 족자, Hanja: 簇
Word: 종로, Hanja: 鍾
Word: 종적, Hanja: 蹤
Word: 준마, Hanja: 駿
Word: 준수하다, Hanja: 俊
Word: 중늙은이, Hanja: 늙
Word: 즐비하다, Hanja: 櫛
Word: 지신밟기, Hanja: 밟
Word: 지척, Hanja: 咫
Word: 진즉, Hanja: 趁
Word: 진지하다, Hanja: 摯
Word: 질, Hanja: 膣
Word: 질곡, Hanja: 桎
Word: 질곡, Hanja: 梏
Word: 집요하다, Hanja: 拗
Word: 쫄면, Hanja: 쫄
Word: 차도, Hanja: 瘥
Word: 차질, Hanja: 蹉
Word: 차질, Hanja: 跌
Word: 참담하다, Hanja: 憺
Word: 참신하다, Hanja: 嶄
Word: 참호, Hanja: 塹
Word: -창, Hanja: 廠
Word: 창포, Hanja: 菖
Word: 창포, Hanja: 蒲
Word: 창해, Hanja: 滄
Word: 처량하다, Hanja: 凄
Word: 처방전, Hanja: 箋
Word: 척, Hanja: 隻
Word: 천식, Hanja: 喘
Word: 철책, Hanja: 柵
Word: 철퇴, Hanja: 槌
Word: 첩, Hanja: 貼
Word: 청국장, Hanja: 麴
Word: 청량하다, Hanja: 亮
Word: 청천벽력, Hanja: 霹
Word: 청천벽력, Hanja: 靂
Word: 초췌하다, Hanja: 憔
Word: 초췌하다, Hanja: 悴
Word: 초췌하다, Hanja: 顦
Word: 초췌하다, Hanja: 顇
Word: 최루탄, Hanja: 淚
Word: 추어탕, Hanja: 鰍
Word: 추장, Hanja: 酋
Word: 추호, Hanja: 毫
Word: 춘부장, Hanja: 椿
Word: 출당, Hanja: 黜
Word: 측간, Hanja: 廁
Word: 치루, Hanja: 瘻
Word: 치열하다, Hanja: 熾
</details>