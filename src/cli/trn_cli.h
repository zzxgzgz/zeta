// SPDX-License-Identifier: GPL-2.0-or-later
/**
 * @file trn_cli.h
 * @author Sherif Abdelwahab (@zasherif)
 *         Phu Tran          (@phudtran)
 *
 * @brief Defines methods and data structs used by the CLI frontend
 *
 * @copyright Copyright (c) 2019 The Authors.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; version 2 of the License.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 */
#pragma once
#pragma GCC system_header

#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <arpa/inet.h>
#include <errno.h>
#include "extern/cJSON.h"
#include "extern/ketopt.h"
#include "rpcgen/trn_rpc_protocol.h"

struct cli_conf_data_t {
	char conf_str[10240]; // 10K conf file is too much anyway
	char intf[21]; // Interface name is 20 char
};

#define print_err(f_, ...)                                                     \
	do {                                                                   \
		fprintf(stderr, f_, ##__VA_ARGS__);                            \
	} while (0)

#define print_msg(f_, ...)                                                     \
	do {                                                                   \
		printf(f_, ##__VA_ARGS__);                                     \
	} while (0)

int trn_cli_read_conf_str(ketopt_t *om, int argc, char *argv[],
			  struct cli_conf_data_t *);

cJSON *trn_cli_parse_json(const char *buf);
int trn_cli_parse_dft(const cJSON *jsonobj, struct rpc_trn_dft_t *dft);
int trn_cli_parse_ftn(const cJSON *jsonobj, struct rpc_trn_ftn_t *ftn);
int trn_cli_parse_ep(const cJSON *jsonobj, struct rpc_trn_endpoint_t *ep);
int trn_cli_parse_zeta_key(const cJSON *jsonobj,
			   struct rpc_trn_zeta_key_t *zeta_key);
int trn_cli_parse_ep_key(const cJSON *jsonobj,
			 struct rpc_trn_endpoint_key_t *ep);
int trn_cli_parse_xdp(const cJSON *jsonobj,
		      struct rpc_trn_xdp_intf_t *xdp_intf);
int trn_cli_parse_tun_intf(const cJSON *jsonobj,
			   struct rpc_trn_tun_intf_t *itf);
int trn_cli_parse_ebpf_prog(const cJSON *jsonobj, rpc_trn_ebpf_prog_t *prog);
int trn_cli_parse_ebpf_prog_stage(const cJSON *jsonobj,
				  rpc_trn_ebpf_prog_stage_t *stage);

int trn_cli_update_dft_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_update_ftn_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_update_ep_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_delete_dft_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_delete_ftn_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_delete_ep_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_get_dft_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_get_ftn_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_get_ep_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_load_transit_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_unload_transit_subcmd(CLIENT *clnt, int argc, char *argv[]);

int trn_cli_load_pipeline_stage_subcmd(CLIENT *clnt, int argc, char *argv[]);
int trn_cli_unload_pipeline_stage_subcmd(CLIENT *clnt, int argc, char *argv[]);

void dump_dft(struct rpc_trn_dft_t *dft);
void dump_ftn(struct rpc_trn_ftn_t *ftn);
void dump_ep(struct rpc_trn_endpoint_t *ep);
