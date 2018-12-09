#include <fstream> // inFile
#include <iostream> // cout
#include <sstream> // tokenStream
#include <unistd.h> // sleep


#include "7.h"

using namespace std;

Workload::Workload()
: m_jobs()
, m_solution()
{
}

void Workload::addJob(JobOrder order)
{
    // Append or Add
    Workload::JobMap::iterator it = m_jobs.find(order.job);
    if (it != m_jobs.end())
    {
        Workload::addUniques(order.reqs, it->second.reqs);
        Workload::addUniques(order.futures, it->second.futures);
    }
    else
    {
        m_jobs[order.job] = order;
    }

    // Create or append futures to the requirements
    for (JobNames::iterator i = order.reqs.begin(); i != order.reqs.end(); i++)
    {
        Workload::JobMap::iterator k = m_jobs.find(*i);
        if (k != m_jobs.end())
        {
            k->second.futures.push_back(order.job);
            k->second.futures.unique();
        }
        else
        {
            JobOrder job(*i);
            job.futures.push_back(order.job);
            m_jobs[*i] = job;
        }
    }
}

void Workload::addUniques(JobNames& fromList, JobNames& toList)
{
    for (JobNames::iterator fromIt = fromList.begin(); fromIt != fromList.end(); fromIt++)
    {
        toList.push_back(*fromIt);
        toList.unique();
    }
}

void Workload::printAllJobs() const
{
    for (JobMap::const_iterator it = m_jobs.begin(); it != m_jobs.end(); it++)
    {
        const JobOrder& job = it->second;
        cout << "Name: " << job.job << endl << "Reqs:";
        for (JobNames::const_iterator reqsIt = job.reqs.begin(); reqsIt != job.reqs.end(); reqsIt++)
        {
            cout << *reqsIt;
        }
        cout << endl << "Futs:";
        for (JobNames::const_iterator futuresIt = job.futures.begin(); futuresIt != job.futures.end(); futuresIt++)
        {
            cout << *futuresIt;
        }
        cout << endl << "Load:" << job.workload << endl;
        cout << endl;
    }
}

// workerID defaults to 0
JobName Workload::getNext(JobName jobName, Worker::WorkerID workerID) const
{
    JobMap::const_iterator it = m_jobs.find(jobName);
    const JobOrder& job = it->second;

    // If not all requirements
    for (JobNames::const_iterator it = job.reqs.begin();
         it != job.reqs.end();
         it++)
    {
        JobMap::const_iterator i = m_jobs.find(*it);
        if (!i->second.solved)
        {
            return Workload::PresNotMet;
        }
    }

    // Current job needs solving or is last
    if (!job.solved || job.futures.size() == 0)
    {
        return jobName;
    }

    // This job is solved. Resolving futures
    JobNames candidates;
    for (JobNames::const_iterator it = job.futures.begin();
         it != job.futures.end();
         it++)
    {
        candidates.push_back(getNext(*it));
    }
    candidates.sort();
    for (JobNames::iterator it = candidates.begin(); it != candidates.end(); it++)
    {
        JobMap::const_iterator i = m_jobs.find(*it);
        if (!i->second.solved && i->second.workload > 0 && (i->second.worker == workerID || i->second.worker == NO_WORKER))
        {
            return i->first;
        }
    }
    return Workload::PresNotMet;
}

// Assignment A
void Workload::solvePuzzle()
{
    JobName rootName = '0';
    JobName endName;

    // Find root and end

    JobOrder root(rootName);

    for (JobMap::iterator it = m_jobs.begin(); it != m_jobs.end(); it++)
    {
        if (it->second.reqs.size() == 0)
        {
            JobName rootName = it->first;
            cout << "root found at " << rootName << ". Appending root 0" << endl;
            it->second.reqs.push_back(root.job);
            root.futures.push_back(it->first);
        }
        if (it->second.futures.size() == 0)
        {
            endName = it->first;
            cout << "end found at " << endName << endl;
        }
    }
    m_jobs[root.job] = root;

    JobName latestNext;
    JobOrder* jobPtr = &m_jobs[rootName];

    cout << "New root: " << rootName << ", end: " << endName << endl;
    bool solving = true;
    while (solving)
    {
        JobName nextJobName = getNext(rootName);
        
        JobMap::iterator i = m_jobs.find(nextJobName);
        JobOrder& nextJob = i->second;
        nextJob.solved = true;
        
        if (rootName != nextJob.job)
        {
            m_solution += nextJob.job;
        }

        if (nextJobName == endName)
        {
            solving = false;
        }
    }
    cout << "Solution: " << m_solution << endl;
}

// Assignment B
void Workload::solvePuzzleWorkers(int numOfWorkers)
{
    JobName rootName = '0';
    JobName endName;

    // Find root and end

    JobOrder root(rootName);

    for (JobMap::iterator it = m_jobs.begin(); it != m_jobs.end(); it++)
    {
        if (it->second.reqs.size() == 0)
        {
            JobName rootName = it->first;
            cout << "root found at " << rootName << ". Appending root 0" << endl;
            it->second.reqs.push_back(root.job);
            root.futures.push_back(it->first);
        }
        if (it->second.futures.size() == 0)
        {
            endName = it->first;
            cout << "end found at " << endName << endl;
        }
    }
    m_jobs[root.job] = root;

    JobOrder* jobPtr = &m_jobs[rootName];

    list<Worker> workers;
    for (int i = 1; i <= numOfWorkers; i++)
    {
        workers.push_back(Worker(i));
    }

    cout << "New root: " << rootName << ", end: " << endName << endl;
    bool solving = true;
    int time = -root.workload; // To be removed from the calculation
    while (solving)
    {
        cout << time << "  ";
        for (list<Worker>::iterator it = workers.begin(); it != workers.end(); it++)
        {
            if (!it->hasJob)
            {
                JobName nextJobName = getNext(rootName, it->getID());
                if (m_jobs.find(nextJobName) != m_jobs.end())
                {   
                    JobMap::iterator i = m_jobs.find(nextJobName);
                    JobOrder& nextJob = i->second;
                    if (nextJob.worker == NO_WORKER)
                    {   
                        nextJob.worker = it->getID();
                        it->setJob(nextJob.job);
                        it->hasJob = true;
                    }
                }
            }
        }
        
        for (list<Worker>::iterator it = workers.begin(); it != workers.end(); it++)
        {
            JobName nextJobName = it->getJob();
            JobMap::iterator i = m_jobs.find(nextJobName);
            JobOrder& nextJob = i->second;
            
            if (nextJob.worker == it->getID())
            {
                nextJob.workload--;
                cout << it->getID() << "(" << nextJob.workload << "|" << it->getJob() << ")  ";
                if (nextJob.workload <= 0)
                {
                    nextJob.solved = true;
                    nextJob.worker = 0;
                    it->hasJob = false;

                    if (rootName != nextJob.job)
                    {
                        m_solution += nextJob.job;
                    }
                    if (nextJobName == endName)
                    {
                        solving = false;
                    }
                }
            }
            else
            {
                 cout << it->getID() << "(.)  ";
            }
        }
        cout << m_solution << endl;
        time++;
    }
    cout << "Solution: " << m_solution << " in " << time << endl;
}

Worker::Worker(WorkerID id)
: m_id(id)
, m_workingOn(NO_JOB)
, hasJob(false)
{

}

Worker::WorkerID Worker::getID()
{
    return m_id;
}

void Worker::setJob(JobName name)
{
    m_workingOn = name;
    hasJob = true;
}

JobName Worker::getJob()
{
    return m_workingOn;
}

vector<string> split(const string& s, char delimiter)
{
    std::vector<std::string> tokens;
    string token;
    istringstream tokenStream(s);
    
    while (getline(tokenStream, token, delimiter))
    {
        tokens.push_back(token);
    }

    return tokens;
}

list<JobOrder> parse(string filename)
{
    const int MAXLINE=256;

    ifstream inFile(filename);
    char oneline[MAXLINE];

    list<JobOrder> orders;

    while (inFile)
    {
        inFile.getline(oneline, MAXLINE);
        vector<string> tokens = split(oneline, ' ');

        JobOrder order(tokens[7][0]);
        order.reqs.push_back(tokens[1][0]);
        orders.push_back(order);
    }

    return orders;
}

int main(int argc, char* argv[])
{
    if (argc != 3)
    {
        cout << "Input is assignment (A or B) followed by file to parse" << endl;
    }

    string assignment = argv[1];
    string inputfile = argv[2];

    cout << "Day 7" << endl;
    Workload workload;
    list<JobOrder> orders = parse(inputfile);

    for (list<JobOrder>::iterator it = orders.begin(); it != orders.end(); it++)
    {
        workload.addJob(*it);
    }

    workload.printAllJobs();

    switch (assignment[0])
    {
        case 'A': 
            workload.solvePuzzle();
            break;
        case 'B':
            workload.solvePuzzleWorkers(5);
            break;
        default:
            cout << "Valid assignments to choose are A or B" << endl;
    }
    
    return 0;
}