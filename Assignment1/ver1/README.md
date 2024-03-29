## Train and Inference with SQLite3

SQLite3을 이용해서 DB로부터 데이터를 읽어오는 학습코드(train.py), 추론코드(inference.py)를 작성해주세요.
 
- 다음 순서대로 작업해 주세요.
    1. train.csv, test.csv를 sqlite3을 이용해서 data.db 파일에 각각 train, test라는 이름으로 적재한다.
    2. data.db 파일에 predict 테이블을 생성하고 pred 라는 이름의 컬럼을 생성한다.
    3. data.db 파일내 train 테이블에서 데이터를 불러와서 StandardScaler로 표준화하고, RandomForestClassifer 모델을 학습하는 train.py를 생성한다.(표준화모듈, 학습모델 을 pickle로 저장한다. )
    4. data.db 파일내 test 테이블에서 (3, 5, 12)번째 row를 불러와서 앞서 train.py에서 생성한 모델로 추론하고 추론결과를 predict 테이블의 pred컬럼에 적재하는 inference.py를 생성한다.
- 제출할 파일은 다음과 같습니다.
    1. `csv_to_db.py` --> train.csv, test.csv파일을 data.db 파일 내 train, test 테이블로 변환하는 코드
    `train.py` --> 모델을 생성하는 코드 (해당 코드 실행시 trans.pkl, model.pkl 생성)
    2. `inference.py` --> 모델을 로드하고 추론결과를 적재하는 코드 (data.db내 predict 테이블을 화면에 출력했을 때 test데이터의 3, 5, 12번째 row의 추론결과가 출력되어야함)
    3. `database.py` --> db파일 내 테이블을 생성하는 함수, db파일에서 특정 row의 데이터를 불러오는 함수가 포함된 파일. (다른 코드들에서 import database로 호출되어야함)