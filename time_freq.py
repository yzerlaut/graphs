
def plot(t, freqs, coefs):
    fig = plt.figure(figsize=(12,6))
    plt.subplots_adjust(wspace=.8, hspace=.5, bottom=.2)
    # signal plot
    plt.subplot2grid((3, 7), (0,0), colspan=6)
    plt.plot(1e3*t, data)
    plt.ylabel('signal');plt.xlabel('time (ms)')
    plt.xlim([1e3*t[0], 1e3*t[-1]])
    # time frequency power plot
    plt.subplot2grid((3, 7), (1,0), rowspan=2, colspan=6)
    c = plt.contourf(1e3*t, freqs, coefs, cmap='PRGn', aspect='auto')
    plt.xlabel('time (ms)')
    plt.ylabel('frequency (Hz)')
    plt.yticks([10, 40, 70]);
    # mean power plot over intervals
    plt.subplot2grid((3, 7), (1, 6), rowspan=2)
    plt.xlabel('power')
    # max of power over intervals
    plt.subplot2grid((3, 8), (1, 7), rowspan=2)
    plt.barh(freqs, np.power(coefs[:,cond],2).mean(axis=1),\
             label='mean')
    plt.plot(np.power(coefs[:,cond],2).mean(axis=1), freqs,\
             label='max.')
    plt.xlabel(' power')
    plt.legend(prop={'size':'small'}, loc=(0.1,1.1))
    plt.show()
