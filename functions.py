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


def plot_shotrecords(recs, model, t0, tn, colorbar=True, titles=None, perc=100):
    ncols = min(3, len(recs))
    nrows = 0
    if ncols < len(recs):
        nrows = 1
    else:
        nrows = int(np.ceil(len(recs)/ncols))

    fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4 * nrows), sharex=True)
    
    if nrows == 1 and ncols == 1:
        axes = [[axes]]
    elif nrows == 1:
        axes = [axes]

    scale = np.max(recs[0])
    for rec in recs:
        scale = max(scale, np.max(rec))
    scale /= 10
    
    is_first = True
    last_plot = None
    for i in range(nrows):
        for j in range(ncols):
            idx = j + i * ncols
            rec = recs[idx]
            title = titles[idx]
            ax = axes[i][j]

            extent = [1e-3*model.origin[0], 1e-3*(model.origin[0] + model.domain_size[0]),
                    1e-3*tn, 1e-3*t0]

            plot = ax.imshow(rec, vmin=-scale, vmax=scale, cmap="gray", extent=extent)
            # perc_val = np.percentile(np.array(rec), perc)
            # perc_mask = (rec <= perc_val)
            # plot = plt.imshow(rec * perc_mask + perc_val*(1 - perc_mask), cmap="gray", extent=extent)
            ax.set_xlabel('X position (km)')
            is_first and ax.set_ylabel('Time (s)')
            is_first = False
            ax.set_title(title)
            # if title:
            #     plt.title(title)
            last_plot = plot
            last_ax = ax

        # Create aligned colorbar on the right
        if colorbar:
            divider = make_axes_locatable(last_ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            plt.colorbar(last_plot, cax=cax)
        plt.show()