from scipy.spatial.distance import pdist
import numpy as np


class DetectPunkto:
    def __init__(self,threshold = 5) -> None:
        
        self.threshold=threshold
        pass
    
    def detect_big_punkto(self,values):
        self.values = sorted(values)
        similar_values = {}
        
        for index in range(len(self.values)):
            for index2 in range(len(self.values)):
                if index == index2:
                    continue
                value=self.values[index]
                if self.values[index] <= self.values[index2]:
                    if self.values[index] + self.threshold >= self.values[index2]:
                        try:
                            similar_values[value] += 1
                        except:
                            similar_values[value] = 1
                            
                elif self.values[index] > self.values[index2]:
                    if self.values[index] - self.threshold <= self.values[index2]:
                        try:
                            similar_values[value] += 1
                        except:
                            similar_values[value] = 1
                else:
                    break
        
        similar_values = {key: value for key, value in reversed(list(similar_values.items()))}
        for key in similar_values:
            if similar_values[key] >= 3:
                return(key)-self.threshold
        return 0
