#include <vector>
#include <map>
#include <list>
#include <string>

typedef char JobName;
typedef std::list<JobName> JobNames;

enum {
    NO_WORKER = 0,
    NO_JOB = 0,
};

struct JobOrder {

    JobOrder(JobName _job = JobName())
    : job(_job)
    , reqs()
    , futures()
    , solved(false)
    , worker(0)
    {
        workload = int(job)-4; // 65 - 4
    }

    JobName job;
    JobNames reqs; // Requirements to finish this job
    JobNames futures; // Jobs that depend on this job
    bool solved;

    // For assignment 2
    int worker; // No worker means free
    int workload; // How many ticks will this work take
};


class Worker 
{
public:
    typedef int WorkerID;
    
    Worker(WorkerID id);

    WorkerID getID();

    void setJob(JobName name);

    JobName getJob();

    bool hasJob;

private:
    WorkerID m_id;

    JobName m_workingOn;
};


class Workload
{
public:
    
    typedef std::map<JobName, JobOrder> JobMap;
    
    static const char PresNotMet = '~';

    Workload();

    void addJob(JobOrder order);

    void printAllJobs() const;

    void solvePuzzle();

    void solvePuzzleWorkers(int numOfWorkers);

private:

    static void addUniques(JobNames& fromList, JobNames& toList);

    JobName getNext(JobName jobName, Worker::WorkerID workerID = 0) const;
    
    JobMap  m_jobs;

    std::string m_solution;
    
};
