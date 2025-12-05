# BMW X5 Driver Behavior Monitor - Phase 1


### Project Structure

```
carmonitor/
├── common/          # Shared modules
│   ├── config.py    # Configuration management
│   ├── logger.py    # Trip logging
│   └── scoring.py   # Driver scoring
├── phase1/          # Phase 1: OBD-II only
│   ├── obd_reader.py    # OBD interface
│   └── obd_monitor.py   # Main app
├── scripts/         # Utility scripts
│   └── test_obd.py      # Connection test
├── config/          # Configuration files
│   └── phase1_config.yaml
└── data/logs/       # Trip data storage
```

### Configuration

Edit `config/phase1_config.yaml` for thresholds and settings.

### Documentation

- Phase 1 details: See `COMPLETE_IMPLEMENTATION_GUIDE.md`
- OBD-II setup: See `obd2_integration_guide.md`

