============================
Generating STRIDE Statistics
============================


    >>> from mdsim.stride import process_line
    >>> structures = process_line('H H H H T T C\n')
    >>> structures
    {'H': 4, 'T': 2, 'C': 1}

    >>> from mdsim.stride import count_helices
    >>> count_helices(structures)
    4
    >>> count_helices({})
    0

    >>> from mdsim.stride import count_all
    >>> count_all(structures)
    7
    >>> count_all({})
    0


    >>> from mdsim.stride import process_file
    >>> file_paths = getfixture('stride_file_paths')
    >>> helices, totals, helices_pcts = process_file(file_paths[0])
    >>> helices
    array([6, 6, 6, 6, 6, 6, 6, 6, 6, 6], dtype=uint64)
    >>> totals
    array([7, 7, 7, 7, 7, 7, 7, 7, 7, 7], dtype=uint64)
    >>> helices_pcts
    array([0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286,
           0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286])

    >>> from mdsim.stride import process_files
    >>> helices, totals, helices_pcts = process_files(file_paths)
    >>> helices.shape
    (4, 10)
    >>> totals.shape
    (4, 10)
    >>> helices
    array([[6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
           [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
           [6, 6, 6, 6, 6, 0, 0, 0, 0, 0],
           [6, 0, 6, 6, 6, 6, 6, 6, 0, 6]], dtype=uint64)
    >>> totals
    array([[7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
           [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
           [7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
           [7, 7, 7, 7, 7, 7, 7, 7, 7, 7]], dtype=uint64)
    >>> helices_pcts
    array([[0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286,
            0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286],
           [0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286,
            0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286],
           [0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286,
            0.        , 0.        , 0.        , 0.        , 0.        ],
           [0.85714286, 0.        , 0.85714286, 0.85714286, 0.85714286,
            0.85714286, 0.85714286, 0.85714286, 0.        , 0.85714286]])


    >>> from mdsim.stride import aggregate_group
    >>> ibu = aggregate_group(helices, totals, [0, 1])
    >>> ibu
    array([[12, 12, 12, 12, 12, 12, 12, 12, 12, 12],
           [14, 14, 14, 14, 14, 14, 14, 14, 14, 14]], dtype=uint64)
    >>> water = aggregate_group(helices, totals, [2, 3])
    >>> water
    array([[12,  6, 12, 12, 12,  6,  6,  6,  0,  6],
           [14, 14, 14, 14, 14, 14, 14, 14, 14, 14]], dtype=uint64)

    >>> from mdsim.stride import group_sum
    >>> ibu_group = [0, 1]
    >>> water_group = [2, 3]
    >>> group_sum(helices, ibu_group)
    array([12, 12, 12, 12, 12, 12, 12, 12, 12, 12], dtype=uint64)
    >>> group_sum(helices, water_group)
    array([12,  6, 12, 12, 12,  6,  6,  6,  0,  6], dtype=uint64)

    >>> from mdsim.stride import group_mean
    >>> group_mean(helices, ibu_group)
    array([6., 6., 6., 6., 6., 6., 6., 6., 6., 6.])
    >>> group_mean(helices_pcts, ibu_group)
    array([0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286,
           0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.85714286])
    >>> group_mean(helices_pcts, water_group)
    array([0.85714286, 0.42857143, 0.85714286, 0.85714286, 0.85714286,
           0.42857143, 0.42857143, 0.42857143, 0.        , 0.42857143])

    >>> from mdsim.stride import stats
    >>> ibu_stats = stats(ibu)
    >>> for (k, v) in ibu_stats.items():
    ...     print(f'{k}:', v)
    y: [0.85714286 0.85714286 0.85714286 0.85714286 0.85714286 0.85714286
     0.85714286 0.85714286 0.85714286 0.85714286]
    y_mean: 0.8571428571428571
    var: 0.0
    helix_count: 120
    structure_count: 140
    steps: 10
    >>> water_stats = stats(water)
    >>> for (k, v) in water_stats.items():
    ...     print(f'{k}:', v)
    y: [0.85714286 0.42857143 0.85714286 0.85714286 0.85714286 0.42857143
     0.42857143 0.42857143 0.         0.42857143]
    y_mean: 0.5571428571428572
    var: 14.76
    helix_count: 78
    structure_count: 140
    steps: 10
