# BMW X5 Driver Behavior Monitor - Phase 1

## Quick Start

**Status:** Code complete ✅ | Testing: Pending (needs car access)

### What Works Now

- ✅ Project structure created
- ✅ All dependencies installed  
- ✅ OBD-II reader module
- ✅ Data logging system
- ✅ Scoring algorithms
- ✅ Main monitor application

### Next Steps

When you have car access:

1. **Pair OBD-II Adapter** (see phase1/README.md)
2. **Test connection:** `python3 scripts/test_obd.py`
3. **Run monitor:** `python3 phase1/obd_monitor.py`

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

