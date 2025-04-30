#include "Logger.h"
#include <chrono>
#include <iomanip>
#include <filesystem>

using namespace std;
namespace fs = std::filesystem;

Logger::Logger() {}
Logger::~Logger() { close(); }

void Logger::openNewFile() {
    fs::create_directories("logs");
    auto t = chrono::system_clock::now();
    auto ts = chrono::system_clock::to_time_t(t);
    ostringstream name;
    name << "logs/log_" << put_time(localtime(&ts), "%Y%m%d_%H%M%S") << ".csv";
    ofs.open(name.str(), ios::out);
    ofs << "t,phi_tail,theta_tail,phi_fin,theta_fin,pos_deg,current_mA,voltage_V,mode\n";
}

void Logger::bufferRow(const vector<string>& row) {
    buffer.push_back(row);
}

void Logger::flush() {
    for(auto &r : buffer) {
        for(size_t i=0;i<r.size();++i) {
            ofs << r[i] << (i+1<r.size()? ',' : '\n');
        }
    }
    ofs.flush();
    buffer.clear();
}

void Logger::close() {
    if(ofs.is_open()) {
        flush();
        ofs.close();
    }
}