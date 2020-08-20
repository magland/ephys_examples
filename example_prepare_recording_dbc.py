import kachery as ka
import kachery_p2p as kp
import neuropixels_data_sep_2020 as nd

# The kachery uri of the raw file obtained via:
# kachery-store /path/to/file.dat
bin_uri = 'sha1://d2fa143e2a6f4f3c6b3b1a216e4540d5f170bc71/128chan_sampleCA1.dat?manifest=18b57e8b0f8f150ec49319a9801ccd3947c73df1'
# Prepare the recording object
# todo: load the probe information for electrode geometry
X1 = dict(
    recording_format='bin1',
    data=dict(
        raw=bin_uri,
        raw_num_channels=134,
        num_frames=600000, # infer from file size and guess of samplerate
        samplerate=30000, # guess
        channel_ids=list(range(0, 128)), # for now
        # The following are placeholders... we need the actual geom file.
        channel_map=dict(zip([str(c) for c in range(0, 128)], [c for c in range(0, 128)])),
        channel_positions=dict(zip([str(c) for c in range(0, 128)], [[c, 0] for c in range(0, 128)]))
    )
)

# Make the list of labbox-ephys recordings
le_recordings = []
le_recordings.append(dict(
    recordingId='128chan_sampleCA1', # just choose an ID (no spaces) to show up in the gui
    recordingLabel='128chan_sampleCA1',
    recordingPath=ka.store_object(X1, basename='128chan_sampleCA1.json'),
    recordingObject=X1,
    description='''
    Example 128-chan recording
    '''.strip()
))

# Create the readonly (static) feed to load using the labbox-ephys GUI
try:
    f = kp.create_feed()
    recordings = f.get_subfeed(dict(documentId='default', key='recordings'))
    for le_recording in le_recordings:
        recordings.append_message(dict(
            action=dict(
                type='ADD_RECORDING',
                recording=le_recording
            )
        ))
    x = f.create_snapshot([dict(documentId='default', key='recordings')])
    print('Labbox-ephys feed URI:', x.get_uri())
finally:
    f.delete()

# Create the spikeinterface recording extractor
R = nd.LabboxEphysRecordingExtractor(X1)

# print information to test
print(R.get_channel_ids())
X = R.get_traces(start_frame=300000, end_frame=310000)
print(X.shape)

# Load the entire file if we want
# local_path = kp.load_file(bin_uri)

# spike sorting will go here