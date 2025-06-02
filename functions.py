# NBVAL_IGNORE_OUTPUT


# NBVAL_IGNORE_OUTPUT

def plot(a, title=None):
    # Some useful definitions for plotting if nbl is set to any other value than zero
    shape_pad = np.array(shape) + 2 * nbl
    origin_pad = tuple([o - s*nbl for o, s in zip(origin, spacing)])
    extent_pad = tuple([s*(n-1) for s, n in zip(spacing, shape_pad)])
    # Note: flip sense of second dimension to make the plot positive downwards
    plt_extent = [origin_pad[0], origin_pad[0] + extent_pad[0],
                origin_pad[1] + extent_pad[1], origin_pad[1]]
    # Plot the wavefields, each normalized to scaled maximum of last time step
    kt = (time_range.num - 2) - 1
    amax = 10 * np.max(np.abs(a.data[kt, :, :]))

    nsnaps = 5
    factor = round(time_range.num / nsnaps)

    fig, axes = plt.subplots(1, 4, figsize=(25, 4), sharex=True)
    fig.suptitle(title, size=15)
    for count, ax in enumerate(axes.ravel()):
        snapshot = factor * (count + 1)
        ax.imshow(np.transpose(a.data[snapshot, :, :]), cmap="seismic", vmin=-amax,
                  vmax=+amax, extent=plt_extent)
        ax.plot(src.coordinates.data[0, 0], src.coordinates.data[0, 1], 'red', linestyle='None', marker='*',
                markersize=8, label="Source")
        ax.grid()
        ax.tick_params('both', length=4, width=0.5, which='major', labelsize=10)
        ax.set_title("Wavefield at t=%.2fms" % (factor*(count + 1)*dt + t0), fontsize=10)
        ax.set_xlabel("X Coordinate (m)", fontsize=10)
        ax.set_ylabel("Z Coordinate (m)", fontsize=10)



# NBVAL_IGNORE_OUTPUT

def plot_interactive_wavefield(wavefield, geometry, title=None):
    # Some useful definitions for plotting if nbl is set to any other value than zero
    shape_pad = np.array(shape) + 2 * nbl
    origin_pad = tuple([o - s*nbl for o, s in zip(origin, spacing)])
    extent_pad = tuple([s*(n-1) for s, n in zip(spacing, shape_pad)])
    # Note: flip sense of second dimension to make the plot positive downwards
    plt_extent = [origin_pad[0], origin_pad[0] + extent_pad[0],
                origin_pad[1] + extent_pad[1], origin_pad[1]]
    # Plot the wavefields, each normalized to scaled maximum of last time step
    kt = (time_range.num - 2) - 1
    amax = 10 * np.max(np.abs(wavefield.data[kt, :, :]))

    # nsnaps = 5
    # factor = round(time_range.num / nsnaps)

    # fig, axes = plt.subplots(1, 4, figsize=(25, 4), sharex=True)
    fig, ax = plt.subplots(1, 1, figsize=(12, 8), sharex=True)
    fig.suptitle(title, size=15)

    ax.imshow(np.transpose(wavefield.data[0, :, :]), cmap="seismic", vmin=-amax,
                vmax=+amax, extent=plt_extent)
    ax.plot(src.coordinates.data[0, 0], src.coordinates.data[0, 1], 'red', linestyle='None', marker='*',
            markersize=8, label="Source")
    ax.grid()
    ax.tick_params('both', length=4, width=0.5, which='major', labelsize=10)
    ax.set_title("Wavefield at t=%.2fms" % (t0), fontsize=10)
    ax.set_xlabel("X Coordinate (m)", fontsize=10)
    ax.set_ylabel("Z Coordinate (m)", fontsize=10)

    def update(frame):
        idx = min(frame * 10, geometry.nt-1)
        ax.imshow(np.transpose(wavefield.data[idx, :, :]), cmap="seismic", vmin=-amax,
                vmax=+amax, extent=plt_extent)

    anim = animation.FuncAnimation(fig=fig, func=update, frames=95)
    anim_html = anim.to_jshtml()
    return HTML(anim_html)