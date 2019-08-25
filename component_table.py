from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# result_set = engine.execute("SELECT * FROM users")
# for r in result_set:
#     print(r)

# 所有的类都要继承自declarative_base这个函数生成的基类
Base = declarative_base()
class components(Base):
    # 定义表名为components
    __tablename__ = 'components'
    # 将id设置为主键，并且默认是自增长的
    id = Column(Integer, primary_key=True)
    # name字段，字符类型，最大的长度是50个字符
    name = Column(String(50))
    version_number = Column(String(20))
    date = Column(String(50))
    url = Column(String(100))

engine = create_engine('postgresql://158.247-app:foobar@localhost:62548/158.247')
Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = Session()
# first_component = components(name='component1',version_number='1.1.1',date='25/8/2019',url='www.google.com')
# session.add(first_component)
