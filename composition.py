from client import avg, count, count0, _pretty_print
from dp import dp_histogram

# This function should expose the true value of some aggregate/query
# by abusing the fact that you can make many such queries.
# query_func is a 0-arguments function, every time you call it, you execute the
# query once and get one set of results.
def expose(query_func):
  headers, many_results = None, []
  # Make many queries and save their results.
  print("Making 200 queries with noise. This may take a minute...")
  for i in range(200):
    headers, results = query_func()
    many_results.append(results)

  exposed_result = []
  num_iterations = len(many_results)
  rows = len(many_results[0])

  # Decide behaviour based on last header name (COUNT vs AVG or other)
  last_header = headers[-1].lower() if headers else ""

  for r in range(rows):
    # collect the noisy values for row r from all iterations
    samples = [ many_results[i][r][-1] for i in range(num_iterations) ]

    # convert to floats (some queries may already be floats)
    samples = [ float(x) for x in samples ]

    # Use the sample mean as the estimator (median is an alternative)
    est = sum(samples) / num_iterations

    # If this is a COUNT-like column, round and clip to non-negative integers
    if "count" in last_header or last_header.startswith("count"):
      value = int(round(est))
      if value < 0:
        value = 0
    else:
      # For AVG (or other real-valued aggregates) keep the float
      # Optionally round to reasonable precision:
      value = float(est)

    labels = tuple(many_results[0][r][:-1])
    exposed_result.append(labels + (value,))

  return headers, exposed_result



if __name__ == "__main__":
  # For testing: if your expose function works, then you should be able
  # to expose the original results of the age and music histogram from 
  # the noised data.
  print("TESTING: the two histograms should be (almost) equal.\n")

  print("Non-noised histogram (from part 1):")
  headers, result = count(["age", "music"], False)
  _pretty_print(headers, result)

  headers, result = expose(lambda: dp_histogram(0.5))
  _pretty_print(headers, result)  

  # Expose the average age per programming level.

  print("Exposing average:")
  headers, result = expose(lambda: avg(["programming"], "age", True))
  _pretty_print(headers, result)
  print("")

  
  # Expose the count of people per programming level.
  '''
  print("Exposing count:")
  headers, result = expose(lambda: count0(["programming"], True))
  _pretty_print(headers, result)
  print("")
  '''
  print("Exposing programming counts (using composition attack)...")
headers_counts, exposed_counts = expose(lambda: count0(["programming"], True))
_pretty_print(headers_counts, exposed_counts)
  
