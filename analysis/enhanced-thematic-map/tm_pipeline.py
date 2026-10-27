"""Replicates bibliometrix::thematicMap() (Cobo et al. 2011 strategic diagram)
on a Scopus CSV: Index Keywords co-occurrence -> association-strength network
-> Louvain communities -> centrality/density ranks. Used to build the
publication figure; mirrors R/thematicMap.R + normalizeSimilarity('association')."""
import pandas as pd, numpy as np, igraph as ig, collections, itertools

def load(path, year_min=None, year_max=None):
    df = pd.read_csv(path)
    if year_min: df = df[(df.Year >= year_min) & (df.Year <= year_max)]
    df = df[df['Index Keywords'].notna()]
    return df

def run(df, n=250, minfreq_pm=5, alpha=0.5, seed=1234):
    N = len(df)
    cnt = collections.Counter()
    doc_terms = []
    for s in df['Index Keywords']:
        ts = sorted({t.strip().lower() for t in s.split(';') if t.strip()})
        doc_terms.append(ts)
        cnt.update(ts)
    top = [t for t, _ in sorted(cnt.items(), key=lambda kv: (-kv[1], kv[0]))[:n]]
    idx = {t: i for i, t in enumerate(top)}
    C = np.zeros((len(top), len(top)))
    for ts in doc_terms:
        ks = [idx[t] for t in ts if t in idx]
        for a in ks:
            C[a, a] += 1
            for b in ks:
                if a != b: C[a, b] += 1
    mf = max(2, int(np.floor(minfreq_pm * N / 1000)))
    keep = np.diag(C) >= mf
    C = C[np.ix_(keep, keep)]
    terms = [t for t, k in zip(top, keep) if k]
    if C.size == 0: return None
    D = np.diag(C).copy()
    with np.errstate(divide='ignore', invalid='ignore'):
        S = np.where(C > 0, C / np.outer(D, D), 0.0)
    S = np.nan_to_num(S)
    m = len(terms)
    edges, w = [], []
    for i in range(m):
        for j in range(i + 1, m):
            if C[i, j] >= 1 and S[i, j] > 0:
                edges.append((i, j)); w.append(S[i, j])
    g = ig.Graph(n=m, edges=edges, directed=False)
    g.vs['name'] = terms
    iso = [v.index for v in g.vs if v.degree() == 0]
    if len(iso) == m: return None
    g.delete_vertices(iso)
    W = np.array(w)
    keep_v = [i for i in range(m) if i not in set(iso)]
    Sg = S[np.ix_(keep_v, keep_v)]
    import random as _random
    _random.seed(seed)
    ig.set_random_number_generator(_random)
    cl = g.community_multilevel(weights=list(W)).membership  # Louvain (multilevel)
    names = g.vs['name']
    sC = np.diag(Sg) * 0 + np.array([D[i] for i in keep_v])
    # term table
    Wnet = Sg.copy(); np.fill_diagonal(Wnet, 0.0)
    g2 = ig.Graph.Weighted_Adjacency(Wnet.tolist(), mode='undirected', loops=False)
    pr = np.array(g2.pagerank(weights=g2.es['weight']))
    lab = []
    for k, t in enumerate(names):
        lab.append(dict(words=t, groups=cl[k], sC=sC[k], pr=pr[k]))
    ldf = pd.DataFrame(lab)
    ldf = ldf[ldf.sC >= mf]
    ldf['rel_freq'] = ldf.groupby('groups').sC.transform(lambda x: x / x.sum())
    ldf['score'] = (alpha * ldf.rel_freq + (1 - alpha) * ldf.pr) * 100
    ldf['freq'] = ldf.groupby('groups').sC.transform('sum')
    # centrality / density (Cobo) on triu(S) pairs
    kv = {t: k for k, t in enumerate(names)}
    grp = dict(zip(ldf.words, ldf.groups))
    acc = collections.defaultdict(lambda: [0.0, 0.0, set()])
    ii = np.triu_indices(len(names), 1)
    for a, b in zip(*ii):
        e = Sg[a, b]
        if e <= 0: continue
        ta, tb = names[a], names[b]
        if ta not in grp or tb not in grp: continue
        ga, gb = grp[ta], grp[bb if False else tb]
        ext = 1.0 if ga != gb else 0.0
        acc[ga][0] += e * ext; acc[ga][1] += e * (1 - ext); acc[ga][2].add(ta)
        acc[gb][0] += e * ext; acc[gb][1] += e * (1 - ext); acc[gb][2].add(tb)
    rows = []
    for gr, (ce, de, ws) in acc.items():
        nq = max(1, len(ws))
        sub = ldf[ldf.groups == gr].sort_values('score', ascending=False)
        rows.append(dict(groups=gr, centrality=ce, density=de / nq * 100,
                         freq=sub.freq.iloc[0],
                         label='\n'.join(sub.words.head(3)),
                         words='\n'.join(f'{w}' for w in sub.words.head(10))))
    cdf = pd.DataFrame(rows)
    if len(cdf) == 0: return None
    cdf['rcentrality'] = cdf.centrality.rank()
    cdf['rdensity'] = cdf.density.rank()
    cdf['cx'] = cdf.rcentrality - cdf.rcentrality.mean()
    cdf['cy'] = cdf.rdensity - cdf.rdensity.mean()
    def quad(r):
        if r.cx >= 0 and r.cy >= 0: return 'Motor'
        if r.cx < 0 and r.cy >= 0: return 'Niche'
        if r.cx >= 0 and r.cy < 0: return 'Basic'
        return 'Emerging'
    cdf['quadrant'] = cdf.apply(quad, axis=1)
    # documents per cluster (docs assigned to cluster sharing most keywords)
    cl_terms = {gr: set(ldf[ldf.groups == gr].words) for gr in cdf.groups}
    docn = collections.Counter()
    for ts in doc_terms:
        best, bg = 0, None
        for gr, st in cl_terms.items():
            o = len(st & set(ts))
            if o > best: best, bg = o, gr
        if bg is not None: docn[bg] += 1
    cdf['docs'] = cdf.groups.map(docn).fillna(0).astype(int)
    return cdf, dict(N=N, mf=mf, nterms=len(names))
