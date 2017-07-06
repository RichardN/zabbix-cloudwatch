#!/usr/bin/python
from basic_discovery import BasicDiscoverer
import re

class Discoverer(BasicDiscoverer):
    def discovery(self, *args):
        regex_lb_long = re.compile('(?:\:\d+\:loadbalancer\/)(.*)$')
        regex_lb_short = re.compile('(?:\:\d+\:loadbalancer\/app\/)([^/]+)/(?:.*)$')
        regex_tg_long = re.compile('(?:\:\d+\:targetgroup\/)(.*)$')

        response = self.client.describe_target_groups()
        data = list()
        for target_group in response["TargetGroups"]:
            for load_balancer in target_group["LoadBalancerArns"]:
                short_balancer_name = regex_lb_short.findall(load_balancer)[0]
                ldd = {
                    "{#TG_IDENTIFIER}":      short_balancer_name + ">" + target_group["TargetGroupName"],
                    "{#TARGET_GROUP_NAME}":  target_group["TargetGroupName"],
                    "{#TARGET_GROUP_ID}":    regex_tg_long.findall(target_group["TargetGroupArn"])[0],
                    "{#BALANCER_NAME}":      short_balancer_name,
                    "{#BALANCER_ID}":        regex_lb_long.findall(load_balancer)[0]
                }
                data.append(ldd)
        return data
