import kachery as ka
import kachery_p2p as kp
import neuropixels_data_sep_2020 as nd
import spikeextractors as se
import spikesorters as ss

bin_uri = 'sha1://d2fa143e2a6f4f3c6b3b1a216e4540d5f170bc71/128chan_sampleCA1.dat?manifest=18b57e8b0f8f150ec49319a9801ccd3947c73df1'
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

le_recordings = []
le_recordings.append(dict(
    recordingId='128chan_sampleCA1',
    recordingLabel='128chan_sampleCA1',
    recordingPath=ka.store_object(X1, basename='128chan_sampleCA1.json'),
    recordingObject=X1,
    description='''
    Example 128-chan recording
    '''.strip()
))

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
    print(x.get_uri())
finally:
    f.delete()

R = nd.LabboxEphysRecordingExtractor(X1)

# print(R.get_channel_ids())
# X = R.get_traces(start_frame=300000, end_frame=310000)
# print(X.shape)

kp.load_file(bin_uri)
S = ss.run_mountainsort4(recording=R)

print(S.get_unit_ids())