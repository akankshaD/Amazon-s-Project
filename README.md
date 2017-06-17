# Interview Scheduler
Interview Scheduling Outlook plugin

References:

http://stackoverflow.com/questions/29338721/interview-scheduling-algorithm

http://stackoverflow.com/questions/19762443/interview-scheduling-algo-with-sub-optimal-solutions

http://stackoverflow.com/questions/11143439/appointment-scheduling-algorithm-n-people-with-n-free-busy-slots-constraint-sa

http://www.geeksforgeeks.org/job-sequencing-problem-set-1-greedy-algorithm/

https://www.careercup.com/question?id=5142448749674496

http://blog.gainlo.co/index.php/2016/07/12/meeting-room-scheduling-problem/

https://hellosmallworld123.wordpress.com/2014/05/30/arranging-the-meeting-room/

Possible approaches to follow:
- Greedy algorithm
- Maximum Bipartite Matching 

Naive Approach:
- Sort and concatenate the free time slots of all interviewers into a single list L on the basis of start time with tagged index of the respective interviewer;
- For all rooms, create minheap of each room on the basis of start time;
- Initialize a priority queue structure P, to hold the output schedule;
- For each slot S_i (st_i, fi_i, I_i) i.e. start time, finish time and Interviewer index in L:
{
    - Repeat until( (slot found) || (fi_i of slot S_i > finish time of slot in R_j (for all j rooms)))
    {
      - Search the slot S_i on the basis of start time in each room minheap R_j;
    }
    - If(Slot found)
    {
      - Remove slot from respective heap and perform reheapify;  
      - Add slot with respective room id in P;
    }
    - Else
    {
      - Continue;
    }
}
  
