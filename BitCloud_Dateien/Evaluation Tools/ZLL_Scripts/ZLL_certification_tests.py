
"""
@testsuite
@description Feature testing test suite

@tags ZLL_CERTIFICATION_TESTS

"""

# Feature tests run retries
runRetries = 1

# Successfull cases
caseList_s = [ 
  '2.1',
  '2.2',
  '2.3',
  '2.4',
  '2.5',
  '2.6',
  '2.7',
  '2.8',
  
  '3.1',
  '3.2',
  '3.3',
  '3.4',
  '3.5',
  '3.6',
  '3.7',
  '3.8',
  '3.9',
  '3.10',
  '3.11',
  '3.12',
  '3.13',
  '3.14',
  '3.15',
  '3.16',
  '3.17',
  '3.18',
  '3.19',
  '3.20',
  '3.21',
  '3.22',

  '4.1',
  '4.2',
  '4.3',
  '4.4',
  '4.5',
  '4.6',
  '4.7',
  '4.8',
  '4.9',
  '4.10',
  '4.11',
  '4.12',
  '4.13',

  '5.2',
  '5.3',
  '5.4',
  '5.5',
  '5.6',
  '5.7',
  '5.8',
  '5.9',
  '5.10',
  '5.11',
  '5.12',
  '5.13',
  '5.14',
]

# Cases which still fails
caseList_f = [
]

caseList_dbg = [
]

caseList = caseList_s
#caseList = caseList_s + caseList_f
#caseList = caseList_dbg

cases = {}
for case in caseList:
  cases[case] = [
    ({}, {})
  ]

for i in range(runRetries):
  runTestCases(cases)
