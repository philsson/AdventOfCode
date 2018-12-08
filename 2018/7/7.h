#include <vector>
#include <map>
#include <list>
#include <string>

typedef char JobName;
typedef std::list<JobName> JobNames;

struct JobOrder {

    JobOrder(JobName _job = JobName())
    : job(_job)
    , reqs()
    , futures()
    , solved(false)
    {}

    JobName job;
    JobNames reqs; // Requirements to finish this job
    JobNames futures; // Jobs that depend on this job
    bool solved;
};

class Workload
{
public:
    
    typedef std::map<JobName, JobOrder> JobMap;
    
    static const char PresNotMet = '|';

    Workload();

    void addJob(JobOrder order);

    void printAllJobs() const;

    void solvePuzzle();

private:

    static void addUniques(JobNames& fromList, JobNames& toList);

    JobName getNext(JobName jobName) const;
    
    JobMap  m_jobs;

    std::string m_solution;
    
};
