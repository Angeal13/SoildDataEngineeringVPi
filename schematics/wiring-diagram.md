graph TB
    subgraph Raspberry Pi 3
        A[USB Ports] --> B[USB to RS485 Converter]
    end

    subgraph Soil Sensor NPK Sensor
        C[RS485 Interface<br/>A+/B- wires]
    end

    subgraph Power Supply
        D[12V DC Power<br/>for Sensor]
    end

    B -->|RS485 Communication| C
    D -->|12V Power| C

    classDef rpi fill:#cce5ff,stroke:#0066cc
    classDef sensor fill:#d4edda,stroke:#28a745
    classDef power fill:#fff3cd,stroke:#ffc107
    
    class A,B rpi
    class C sensor
    class D power
