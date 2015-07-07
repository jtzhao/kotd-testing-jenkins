#!/bin/bash
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************


# Description: print debug message to stderr
# Parameters:   $1 - function name
#               $2 - message
debug()
{
        if [[ "$DEBUG" == "true" ]]; then
                echo "[DEBUG] $1: $2" 1>&2
        fi
}


# Description: run command and print debug info
# Parameters:   $1 - function name
#               $2 - cmd
run()
{
        debug $1 "# $2"
        output=$(eval "$2")
        ret=$?
        echo "$output"
        return $ret
}

# Description: Compare 2 package versions(e.g. 3.12.44-4.1.g84afcfd.ppc64le vs 3.11.44-4.2.g84afcfd.ppc64le)
#       Return 0 immediately when meets alphabetical letters(e.g. g84afcfd won't be compared) 
# Parameter:    $1 - version 1
#               $2 - version 2
# Return:       0 - two versions are equal
#               1 - version 1 is greater than version 2
#               255 - version 1 is smaller than version 2
version_cmp() {
        ver1=$(echo "$1" | sed -e 's/_-/./g')
        ver2=$(echo "$2" | sed -e 's/_-/./g')
        declare -i i=1
        while [[ 1 ]]; do
                part1=$(echo "$ver1" | cut -d'.' -f${i} | grep -P '^\d+$')
                part2=$(echo "$ver2" | cut -d'.' -f${i} | grep -P '^\d+$')
                if [[ -z "$part1" ]] || [[ -z "$part2" ]]; then
                        return 0
                fi
                if [[ "$part1" -gt "$part2" ]]; then
                        debug $FUNCNAME "$1 > $2"
                        return 1
                elif [[ "$part1" -eq "$part2" ]]; then
                        i+=1
                else
                        debug $FUNCNAME "$1 < $2"
                        return 255 
                fi
        done
        debug $FUNCNAME "$1 = $2"
        return 0
}
