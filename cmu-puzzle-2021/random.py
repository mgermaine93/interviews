# # SAMPLE OUTPUT:
# from math import ceil, floor
# from decimal import Decimal, ROUND_UP

# results = [
#     {
#         "host": "npr.org",
#         "average_rtt": "25.273ms",
#         "raw_results": [
#             {
#                 "seq": 1,
#                 "rtt": "21.466"
#             },
#             {
#                 "seq": 2,
#                 "rtt": "29.081"
#             }
#         ]
#     },
#     {
#         "host": "cmu.edu",
#         "average_rtt": "57.008ms",
#         "raw_results": [
#             {
#                 "seq": 1,
#                 "rtt": "57.182"
#             },
#             {
#                 "seq": 2,
#                 "rtt": "56.834"
#             }
#         ]
#     },
#     {
#         "host": "microsoft.com",
#         "average_rtt": "10000.000ms",
#         "raw_results": [
#             {
#                 "seq": 1,
#                 "rtt": "10000.000"
#             },
#             {
#                 "seq": 2,
#                 "rtt": "10000.000"
#             }
#         ]
#     }
# ]


# # def find_avg_rtt(results):
# #     rounded_results = []
# #     for result in results:
# #         rtt = float(result["average_rtt"][:-2])
# #         rounded_rtt = Decimal(rtt).quantize(Decimal('.01'), rounding=ROUND_UP)
# #         print(rounded_rtt, type(rounded_rtt))
# #         rounded_results.append(rounded_rtt)
# #     sorted_results = sorted(rounded_results, reverse=True)
# #     return [str(rtt) for rtt in sorted_results]
# def find_avg_rtt(result):
#     """ Returns a decimal """
#     rtt = float(result["average_rtt"][:-2])
#     rounded_rtt = Decimal(rtt).quantize(Decimal('.01'), rounding=ROUND_UP)
#     return rounded_rtt


# result = {
#     "host": "microsoft.com",
#     "average_rtt": "10000.000ms",
#     "raw_results": [
#             {
#                 "seq": 1,
#                 "rtt": "10000.000"
#             },
#         {
#                 "seq": 2,
#                 "rtt": "10000.000"
#         }
#     ]
# }

# print(find_avg_rtt(result))

# # print(find_avg_rtt(results))
# # sorted_list = sorted(results, key=find_avg_rtt, reverse=False)
# # print(sorted_list)
