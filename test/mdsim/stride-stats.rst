============================
Analyzing simulation results
============================


STRIDE
======

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

    >>> from mdsim.stride import helix_denature_time
    >>> y_raw = helices_pcts[2]
    >>> t_h = helix_denature_time(y_raw)
    >>> t_h
    4
    >>> y_raw[:t_h]
    array([0.85714286, 0.85714286, 0.85714286, 0.85714286])
    >>> y_raw[t_h:]
    array([0.85714286, 0.        , 0.        , 0.        , 0.        ,
           0.        ])

    >>> from mdsim.stride import split_helix_timeline
    >>> y1, y2 = split_helix_timeline(y_raw, 1)
    >>> y1
    array([0.85714286])
    >>> y2
    array([0.85714286, 0.85714286, 0.85714286, 0.85714286, 0.        ,
           0.        , 0.        , 0.        , 0.        ])
    >>> y1, y2 = split_helix_timeline(y_raw)
    >>> (y1 == y_raw[:t_h]).all()
    True
    >>> (y2 == y_raw[t_h:]).all()
    True

    >>> from mdsim.stride import split_helix_timeline_all
    >>> ys_initial, ys_final = split_helix_timeline_all(helices_pcts)
    >>> for y in ys_initial:
    ...     y.shape
    (9,)
    (9,)
    (4,)
    (9,)
    >>> for y in ys_final:
    ...     y.shape
    (1,)
    (1,)
    (6,)
    (1,)
    >>> (ys_initial[2] == y1).all()
    True
    >>> (ys_final[2] == y2).all()
    True

    >>> from mdsim.stride import helix_timeline_means
    >>> ys_initial, ys_final = helix_timeline_means(helices_pcts)
    >>> ys_initial
    [0.8571428571428571, 0.8571428571428571, 0.8571428571428571, 0.6666666666666666]
    >>> ys_final
    [0.8571428571428571, 0.8571428571428571, 0.14285714285714285, 0.8571428571428571]


Contacts
========

    >>> from mdsim.stride import process_contact_line
    >>> process_contact_line('1 2 3 4\n')
    [1, 2, 3, 4]

    >>> from mdsim.stride import process_contact_file
    >>> file_paths = getfixture('contact_file_paths')
    >>> for row in process_contact_file(file_paths[0]):
    ...     print(row)
    [1, 1, 2, 0, 0, 1, 1]
    [1, 1, 2, 0, 1, 0, 0]
    [1, 1, 2, 1, 0, 0, 0]
    [1, 1, 2, 1, 0, 0, 1]
    [1, 1, 2, 1, 0, 1, 0]
    [1, 1, 2, 1, 0, 1, 1]
    [1, 1, 2, 1, 1, 0, 0]
    [1, 1, 2, 1, 1, 1, 0]
    [1, 1, 2, 1, 1, 1, 1]
    [1, 1, 2, 1, 2, 0, 1]
    >>> for row in process_contact_file(file_paths[1]):
    ...     print(row)
    [1, 0, 3, 2, 0, 1, 0]
    [1, 0, 3, 2, 0, 1, 2]
    [1, 1, 0, 0, 0, 0, 0]
    [1, 1, 0, 0, 0, 0, 1]
    [1, 1, 0, 0, 0, 1, 0]
    [1, 1, 0, 0, 0, 1, 1]
    [1, 1, 0, 0, 1, 0, 0]
    [1, 1, 0, 0, 1, 0, 1]
    [1, 1, 0, 0, 1, 1, 0]
    [1, 1, 0, 0, 1, 1, 1]

    >>> from mdsim.stride import process_contact_files
    >>> contacts = process_contact_files(file_paths)
    >>> contacts.shape
    (2, 10, 7)
    >>> c1, c2 = contacts
    >>> c1
    array([[1, 1, 2, 0, 0, 1, 1],
           [1, 1, 2, 0, 1, 0, 0],
           [1, 1, 2, 1, 0, 0, 0],
           [1, 1, 2, 1, 0, 0, 1],
           [1, 1, 2, 1, 0, 1, 0],
           [1, 1, 2, 1, 0, 1, 1],
           [1, 1, 2, 1, 1, 0, 0],
           [1, 1, 2, 1, 1, 1, 0],
           [1, 1, 2, 1, 1, 1, 1],
           [1, 1, 2, 1, 2, 0, 1]], dtype=uint64)
    >>> c2
    array([[1, 0, 3, 2, 0, 1, 0],
           [1, 0, 3, 2, 0, 1, 2],
           [1, 1, 0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0, 0, 1],
           [1, 1, 0, 0, 0, 1, 0],
           [1, 1, 0, 0, 0, 1, 1],
           [1, 1, 0, 0, 1, 0, 0],
           [1, 1, 0, 0, 1, 0, 1],
           [1, 1, 0, 0, 1, 1, 0],
           [1, 1, 0, 0, 1, 1, 1]], dtype=uint64)

    >>> from mdsim.stride import mean_residue_contact_frequency
    >>> mean_residue_contact_frequency(c1)
    array([1. , 1. , 2. , 0.8, 0.6, 0.5, 0.5])
    >>> mean_residue_contact_frequency(c2)
    array([1. , 0.8, 0.6, 0.4, 0.4, 0.6, 0.6])

    >>> from mdsim.stride import total_mean_residue_contact_frequency
    >>> total_mean_residue_contact_frequency(contacts)
    array([1.  , 0.9 , 1.3 , 0.6 , 0.5 , 0.55, 0.55])

    >>> from mdsim.stride import split_contact_timeline
    >>> c1_initial, c1_final = split_contact_timeline(c1, 5)
    >>> c1_initial
    array([[1, 1, 2, 0, 0, 1, 1],
           [1, 1, 2, 0, 1, 0, 0],
           [1, 1, 2, 1, 0, 0, 0],
           [1, 1, 2, 1, 0, 0, 1],
           [1, 1, 2, 1, 0, 1, 0]], dtype=uint64)
    >>> c1_final
    array([[1, 1, 2, 1, 0, 1, 1],
           [1, 1, 2, 1, 1, 0, 0],
           [1, 1, 2, 1, 1, 1, 0],
           [1, 1, 2, 1, 1, 1, 1],
           [1, 1, 2, 1, 2, 0, 1]], dtype=uint64)

    >>> from mdsim.stride import split_contact_timeline_all
    >>> contacts_initial, contacts_final = split_contact_timeline_all(
    ...     contacts, 5)
    >>> len(contacts_initial)
    2
    >>> contacts_initial[0]
    array([[1, 1, 2, 0, 0, 1, 1],
           [1, 1, 2, 0, 1, 0, 0],
           [1, 1, 2, 1, 0, 0, 0],
           [1, 1, 2, 1, 0, 0, 1],
           [1, 1, 2, 1, 0, 1, 0]], dtype=uint64)
    >>> contacts_initial[1]
    array([[1, 0, 3, 2, 0, 1, 0],
           [1, 0, 3, 2, 0, 1, 2],
           [1, 1, 0, 0, 0, 0, 0],
           [1, 1, 0, 0, 0, 0, 1],
           [1, 1, 0, 0, 0, 1, 0]], dtype=uint64)
    >>> len(contacts_final)
    2
    >>> contacts_final[0]
    array([[1, 1, 2, 1, 0, 1, 1],
           [1, 1, 2, 1, 1, 0, 0],
           [1, 1, 2, 1, 1, 1, 0],
           [1, 1, 2, 1, 1, 1, 1],
           [1, 1, 2, 1, 2, 0, 1]], dtype=uint64)
    >>> contacts_final[1]
    array([[1, 1, 0, 0, 0, 1, 1],
           [1, 1, 0, 0, 1, 0, 0],
           [1, 1, 0, 0, 1, 0, 1],
           [1, 1, 0, 0, 1, 1, 0],
           [1, 1, 0, 0, 1, 1, 1]], dtype=uint64)
    >>> total_mean_residue_contact_frequency(contacts_initial)
    array([1. , 0.8, 1.6, 0.7, 0.1, 0.5, 0.5])
    >>> total_mean_residue_contact_frequency(contacts_final)
    array([1. , 1. , 1. , 0.5, 0.9, 0.6, 0.6])
