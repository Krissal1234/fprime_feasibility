// ======================================================================
// \title  TcpDriver.cpp
// \author krissal1234
// \brief  cpp file for TcpDriver component implementation class
// ======================================================================

#include "FprimeSyncbench/Components/TcpDriver/TcpDriver.hpp"

namespace FprimeSyncbench {

// ----------------------------------------------------------------------
// Component construction and destruction
// ----------------------------------------------------------------------

TcpDriver ::TcpDriver(const char* const compName) : TcpDriverComponentBase(compName) {}

TcpDriver ::~TcpDriver() {}

// ----------------------------------------------------------------------
// Handler implementations for typed input ports
// ----------------------------------------------------------------------

void TcpDriver ::dataIn_handler(FwIndexType portNum, const FprimeSyncbench::BenchData& data) {
    // TODO
}

// ----------------------------------------------------------------------
// Handler implementations for commands
// ----------------------------------------------------------------------

void TcpDriver ::CONNECT_TCP_cmdHandler(FwOpcodeType opCode,
                                        U32 cmdSeq,
                                        const Fw::CmdStringArg& hostname,
                                        U32 hostport) {
    // TODO
    this->cmdResponse_out(opCode, cmdSeq, Fw::CmdResponse::OK);
}

}  // namespace FprimeSyncbench
