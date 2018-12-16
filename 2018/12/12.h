#include <bitset>
#include <map>
#include <string>

class PlantPopulation
{
public:
    //typedef std::bitset<5> Bit5;
    
    typedef uint8_t Formula;

    PlantPopulation(std::string initialState);

    void appendFormula(const std::string& pattern, const std::string& result);

    uint64_t evolve();

    void printPopulation();

private:

    template <class T>
    T stringtobits(const std::string& input, bool center = false);

    template <class T>
    std::string bitstostring(const T& input, int bitSize = 0);

    const std::string m_initialState;
    uint64_t m_state;

    std::map<Formula, Formula> m_formulas;

};