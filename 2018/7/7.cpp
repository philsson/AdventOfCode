#include <fstream> // inFile
#include <iostream> // cout
#include <sstream> // tokenStream

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
            JobOrder job;
            job.job = *i;
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
        cout << endl << endl;
    }
}

JobName Workload::getNext(JobName jobName) const
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

    if (!job.solved || job.futures.size() == 0)
    {
        return jobName;
    }

    JobNames candidates;
    for (JobNames::const_iterator it = job.futures.begin();
         it != job.futures.end();
         it++)
    {
        candidates.push_back(getNext(*it));
    }
    candidates.sort();
    return candidates.front();
}

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
        //cout << oneline << endl;
        
        vector<string> tokens = split(oneline, ' ');
        //cout << tokens[1] << "," << tokens[7] << endl;

        JobOrder order;
        order.job = tokens[7][0];
        order.reqs.push_back(tokens[1][0]);
        orders.push_back(order);
    }

    return orders;
}

int main(int argc, char* argv[])
{
    cout << argv[1] << endl;

    string inputfile = (argc > 0) ? argv[1] : "test_input.txt";

    cout << "Day 7" << endl;
    Workload workload;
    list<JobOrder> orders = parse(inputfile);

    for (list<JobOrder>::iterator it = orders.begin(); it != orders.end(); it++)
    {
        workload.addJob(*it);
    }

    //workload.printAllJobs();

    workload.solvePuzzle();
}