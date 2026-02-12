module FprimeSyncbench {
    @ Tcp driver that connects outgoing data to a server
    active component TcpDriver {


        async input port dataIn: BenchDataPort

        async command CONNECT_TCP(hostname: string, hostport: U32)


        ###############################################################################
        # Standard AC Ports: Required for Channels, Events, Commands, and Parameters  #
        ###############################################################################
        @ Port for requesting the current time
        time get port timeCaller

        @ Enables command handling
        import Fw.Command


    }
}