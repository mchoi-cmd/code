To start the server,
- install `Node.js` https://nodejs.org/en/download
- install express library first by type `npm install express`. (You might need administrator access)
- type `node server.js`

To run the python test,
- install python 3.10
- type `pytest test_server.py -v`

you should get the following output
```
% pytest test_server.py -v
====================================================================================== test session starts ======================================================================================
platform darwin -- Python 3.10.10, pytest-7.3.2, pluggy-1.0.0 -- /Library/Frameworks/Python.framework/Versions/3.10/bin/python3
cachedir: .pytest_cache
rootdir: /Users/mchoi/Documents/GitHub/taketwoassessment
plugins: playwright-0.3.0, base-url-2.0.0
collected 6 items

test_server.py::test_post_positive_multiple_items PASSED                                                                                                                                  [ 16%]
test_server.py::test_post_positive_single_item PASSED                                                                                                                                     [ 33%]
test_server.py::test_post_positive_no_item PASSED                                                                                                                                         [ 50%]
test_server.py::test_post_no_data PASSED                                                                                                                                                  [ 66%]
test_server.py::test_invalid_get_path PASSED                                                                                                                                              [ 83%]
test_server.py::test_invalid_put_path PASSED                                                                                                                                              [100%]

======================================================================================= 6 passed in 0.09s =======================================================================================

```