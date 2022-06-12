# comparative-challenge
Take home challenge

I found the best way to parallelize the algorithm across multiple cores,
by computing each metric on separate core.

Time for computing 2 metrics using 2 cores:
```
Size is 10000
 combine: 0.016937971115112305 seconds
 parallel_combine: 0.6022148132324219 seconds
Size is 100000
 combine: 0.07283401489257812 seconds
 parallel_combine: 0.629472017288208 seconds
Size is 1000000
 combine: 0.5487642288208008 seconds
 parallel_combine: 1.043030023574829 seconds
Size is 10000000
 combine: 5.4914937019348145 seconds
 parallel_combine: 5.475867033004761 seconds
Size is 20000000
 combine: 13.785660028457642 seconds
 parallel_combine: 12.470846891403198 seconds
Size is 30000000
 combine: 20.93286895751953 seconds
 parallel_combine: 23.58819603919983 seconds
```

Time for computing 6 metrics using 6 cores:
```
Size is 10000
 combine: 0.05186200141906738 seconds
 parallel_combine: 0.6373152732849121 seconds
Size is 100000
 combine: 0.19961071014404297 seconds
 parallel_combine: 0.7071428298950195 seconds
Size is 1000000
 combine: 1.598417043685913 seconds
 parallel_combine: 1.3687620162963867 seconds
Size is 10000000
 combine: 16.698230028152466 seconds
 parallel_combine: 10.704653024673462 seconds
Size is 20000000
 combine: 41.22689700126648 seconds
 parallel_combine: 43.38397717475891 seconds
```

Parallel version is slower than serial version on small data
(overhead from data exchange between cores),
but starting from 10^7 it speeds up computing.
Processing of data bigger 10^8 has similar speed on both versions,
or parallel version is even worse.
