import requests
import json
import re

cookie = 'cookie，随便找一个请求的header里面就有'
reqtoken = '输入登录时的reqtoken，第一个请求就有'

# 获取答案
url = "https://www.2-class.com/api/exam/getTestPaperList?courseId={}"

headers = {
  'Cookie': cookie,
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0'
}


# 提交
posturl = "https://www.2-class.com/api/exam/commit"


postheaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
    'Cookie': cookie,
    'Content-Type': 'application/json'
}
gradeList = ['五年级', '六年级', '七年级', '八年级', '九年级', '高一', '高二', '中职一', '中职二']
courseIdList = []
print('>> 正在查找所有课程资源...')
for gradeName in gradeList:
    res = requests.request(
        "GET", 'https://www.2-class.com/api/course/getHomepageCourseList?grade={}&pageNo=1&pageSize=66&sort='.format(gradeName,))
    # print(res.text)
    t = res.text
    word = r'courseId'
    a = [m.start() for m in re.finditer(word, t)]
    for i in a:
        try:
            courseIdList.append(int(t[i+10:i+14]))
        except:
            pass
# print(courseIdList)
# exit()
print('<< 已查找到课程数量: '+str(len(courseIdList)))

for i,courseId in enumerate(courseIdList):
    endsay = ' - {}/{}'.format(i+1,len(courseIdList))
    print('\n>> 正在答题  Id: '+str(courseId))
    urlt = url.format(courseId)
    ans = requests.request("GET", urlt, headers=headers, data={})
    t = ans.text
    try:
        err = json.loads(t)['data']['errorMsg']
        print('<< 错误: '+err+endsay if err else '<< 获取题目成功'+endsay)
        continue
    except:
        pass
    try:
        dic = json.loads(t)
        examCommitReqDataList = []
        for i, item in enumerate(dic['data']['testPaperList']):
            answer = item['answer']
            examCommitReqDataList.append({
                "examId": i+1,
                "answer": answer
            })
    except:
        print('<< 错误: 答案获取错误'+endsay)
        continue
    postpayload = json.dumps({
        "courseId": courseId,
        "examCommitReqDataList": examCommitReqDataList,
        "exam": "course",
        "reqtoken": reqtoken
    })
    res = requests.request("POST", posturl, headers=postheaders, data=postpayload)
    j = json.loads(t)
    if j['success']:
        print("<< 答题成功, 满分!"+endsay)
        
print(">> 正在完成期末考试")
url = "https://www.2-class.com/api/question/commit"

payload = json.dumps({
  "list": [
    {
      "questionId": 692,
      "questionContent": "D"
    },
    {
      "questionId": 693,
      "questionContent": "C"
    },
    {
      "questionId": 694,
      "questionContent": "B"
    },
    {
      "questionId": 695,
      "questionContent": "D"
    },
    {
      "questionId": 696,
      "questionContent": "D"
    },
    {
      "questionId": 697,
      "questionContent": "B"
    },
    {
      "questionId": 698,
      "questionContent": "C"
    },
    {
      "questionId": 699,
      "questionContent": "C"
    },
    {
      "questionId": 700,
      "questionContent": "B"
    },
    {
      "questionId": 701,
      "questionContent": "D"
    }
  ],
  "exam": "final",
  "reqtoken": reqtoken
})
headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
  'Cookie': cookie,
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print("<< 成功完成期末考试。服务器返回: \n"+json.dumps(json.loads(response.text)['data'],ensure_ascii=False,indent=2))
