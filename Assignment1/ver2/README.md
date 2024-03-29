## Train and Inference with SQLite3

1. [수정할 코드]들을 수정해서 제출해 주세요. 
     - sqlite3을 이용해서 데이터를 추출, 적재, 화면출력하는 함수를 갖고 있는 `database.py` 코드를 생성
     - `database.py`를 호출해서 [수정할 코드]들을 수정 --> 코드 간소화 
     - `create_tables.py` 에서 predict 테이블을 생성할때 predict 컬럼만 생성하지 말고 X 컬럼들도 같이 적재할수 있도록 준비. 
     - 3.batch_run.py, run.py를 수정해서 predict 테이블에 추론할 X 컬럼들과 추론 결과(predict)가 적재 되도록 수정.
2. `run.py`에서 100건의 online추론이 진행되도록 수정해 주세요. (`inference.py`도 수정해야 효율화가 됨)
    - Test 테이블에서 랜덤하게 데이터 1개 추출해서 추론한 후 predict 테이블에 적재 --> 100번 반복 --> 100개의 추론결과가 predict에 적재되도록
    - 추론을 실행한 후 predict테이블에 X값들과 추론결과(predict)가 같이 적재되도록 수정
3. 코드들이 완성되면, 다음의 순서로 실행했을 때 에러 없이 실행되어야 합니다. 
	```
	python3 1.create_tables.py
	python3 2.train.py
	python3 3.batch_run.py
	python3 run.py
	```
4. 위 3을 진행한 후 steel.db 파일의 predict 테이블을 출력하면 
    X컬럼들과 predict컬럼이 출력되고, 행의 개수는 583+100=683개가 되어야 합니다. 

---
**[수정할 코드]**
- `1.create_tables.py`
- `2.train.py`
- `3.batch_run.py`
- `run.py` 
- `inference.py`
  
**[추가로 생성할 코드]**
- `database.py` 
