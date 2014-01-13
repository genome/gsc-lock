local queue_max_timeout = function(lock_queue_timeout_types,
        lock_queue_timeouts)
    local max_expire = 0
    local max_pexpire = 0

    for i, request_id in pairs(redis.call('HKEYS', lock_queue_timeout_types)) do
        local timeout_type = redis.call('HGET', lock_queue_timeout_types,
            request_id)
        local timeout = redis.call('HGET', lock_queue_timeouts, request_id)
        if timeout_type == 'EXPIRE' then
            max_expire = math.max(max_expire, timeout)
        else
            max_pexpire = math.max(max_pexpire, timeout)
        end
    end

    if max_expire * 1000 > max_pexpire then
        return 'EXPIRE', max_expire
    else
        return 'PEXPIRE', max_pexpire
    end
end

local queue_update_timeout = function(lock_queue,
        lock_queue_timeout_types, lock_queue_timeouts,
        lock_queue_data)
    local timeout_type, timeout = queue_max_timeout(lock_queue_timeout_types,
        lock_queue_timeouts)

    redis.call(timeout_type, lock_queue, timeout)
    redis.call(timeout_type, lock_queue_timeout_types, timeout)
    redis.call(timeout_type, lock_queue_timeouts, timeout)
    redis.call(timeout_type, lock_queue_data, timeout)

    return
end

local queue_promote = function(lock_key, lock_queue, lock_queue_timeout_types,
        lock_queue_timeouts, lock_queue_data)

    if redis.call('EXISTS', lock_key) ~= 0 then
        return -1 -- lock still valid

    else
        if redis.call('LLEN', lock_queue) == 0 then
            redis.call('DEL', lock_queue_timeout_types, lock_queue_timeouts,
                lock_queue_data)

            return 0 -- queue empty

        else
            local request_id = redis.call('LPOP', lock_queue)
            local timeout_type = redis.call('HGET', lock_queue_timeout_types,
                request_id)
            redis.call('HDEL', lock_queue_timeout_types, request_id)

            local timeout = redis.call('HGET', lock_queue_timeouts, request_id)
            redis.call('HDEL', lock_queue_timeouts, request_id)

            local data = redis.call('HGET', lock_queue_data, request_id)
            redis.call('HDEL', lock_queue_data, request_id)

            redis.call('HMSET', lock_key,
                       'request_id', request_id,
                       'timeout_type', timeout_type,
                       'timeout', timeout,
                       'data', data)
            redis.call(timeout_type, lock_key, timeout)

            return 1 -- successful promotion
        end
    end
end

local queue_insert = function(lock_queue,
        lock_queue_timeout_types, lock_queue_timeouts,
        lock_queue_data,
        request_id, timeout_type, timeout, data)

    redis.call('LPUSH', lock_queue, request_id)
    redis.call('HSET', lock_queue_timeout_types, request_id, timeout_type)
    redis.call('HSET', lock_queue_timeouts, request_id, timeout)
    redis.call('HSET', lock_queue_data, request_id, data)

    return
end