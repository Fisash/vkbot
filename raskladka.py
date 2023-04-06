rus = list("йцукенгшщзхъфывапролджэячсмитьбю")
eng = list("qwertyuiop[]asdfghjkl;'zxcvbnm,.")

class LayoutChanger():

    def change(_data):
        result = _data;
        to_rus = True
        for i in range(len(rus)):
            if rus[i] in _data:
                to_rus = False
                break
        for i in range(len(rus)):
            if to_rus:
                result =  result.replace(eng[i], rus[i])
            else:
                result =  result.replace(rus[i], eng[i])
        return result
