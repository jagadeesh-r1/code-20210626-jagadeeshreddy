import json
import bisect
# import multiprocessing as mp
from constants import bmi_scale,bmi_category,catch_exceptions

class BodyMassIndex:
    
    def __init__(self) -> None:
        # self.__pool = mp.Pool()
        pass

    @catch_exceptions
    def __convert_m_to_cm(self,height):
        return height/100 

    @catch_exceptions
    def __calculate_bmi(self,record):
        height = self.__convert_m_to_cm(record.get("HeightCm"))
        weight = record.get("WeightKg")
        BMI = round(weight / (height**2),2)
        bmi_info = bmi_category.get(bisect.bisect_left(bmi_scale,(BMI+0.01))-1)
        bmi_info["BMI"] = BMI
        return bmi_info

    @catch_exceptions
    def __process_data(self,records):
        # self.__pool.map(self.__calculate_bmi,records)
        # self.__pool.close()
        for i in records:
            i.update(self.__calculate_bmi(i))
        return records

    @catch_exceptions
    def process_start(self,input_file_path,output_file_path):
        if input_file_path == None or output_file_path  == None:
            raise Exception("Input file or Output file paths does not exist")
        
        with open(input_file_path,'rb') as input_file:
            input_records = json.load(input_file)

        processed_data = self.__process_data(input_records)
        # print(processed_data)
        with open(output_file_path,'w') as outfile:
            json.dump(processed_data,outfile,indent=4)

