#!/usr/bin/env python
# coding: utf-8

# In[ ]:


class Time_Series_Model:
    """
    원하는 기간을 입력하면 해당 기간에 맞춰 입력 데이터셋 생성
    """
    def __init__(self, term):
        self.term=term
    def is_exist(self, company_start_year):
        """
    해당 년도에 회사가 존재했는지에 관한 2000~2018년 까지 불리언 배열을 생성하는 함수
    company_start_year은 각 회사의 설립년도가 나와있는 데이터셋(2000년 이전에 설립된 회사는 2000년으로)"""
        
        num_company = company_start_year.shape[0]
        
        # 각 회사가 해당 년도에 있었는지를 반환하는 불리언 배열
        company_exist = [[] for i in range(num_company)] 
        for i in range(num_company):
            for year in range(2000,2019):

                # 만약 존재하면 1을 추가
                if company_start_year["start_year"][i]<=year: 
                    company_exist[i].append(True)

                # 만약 존재하지 않았을 시 0을 추가
                else:
                    company_exist[i].append(False)

        return np.array(company_exist)

    def make_dataset(self,data):
        company_exist = self.is_exist(company_start_year)
        cv = 18-self.term+1 # fold 개수

        for i in range(cv):
            # 해당 년도(시작년도 기준-2012~2014라면 2012 기준)에 존재하는 회사만을 추출
            one_bool_array = company_exist[:,i]
            bool_array = np.tile(one_bool_array,self.term)
            
            # 존재하는 회사 데이터 추출
            sub_data = np.array(data[i*(2191):2191*(i+self.term)][bool_array])
            num_data = one_bool_array.sum() # 해당 년도에 존재하는 회사 개수
            
            # 데이터 shape 변환
            sub_data = np.concatenate([sub_data[num_data*t:num_data*(t+1)] for t in range(term)], axis=1)
            
            X,y = sub_data[:,:-1], sub_data[:,-1]
            yield X,y
    

